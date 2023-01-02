import org.apache.spark.sql.functions.{struct, to_json}

val inMoviesDataPath = "data/ml-latest-small/movies.csv"
val inTagsDataPath = "data/ml-latest-small/tags.csv"
val inRatingsDataPath = "data/ml-latest-small/ratings.csv"
val outDataPath = "data/ml-latest-small/movies_denormalized.csv"

// Read source data
val inMoviesDF = spark.read.format("csv").option("header", "true").load(inMoviesDataPath)
val inTagsDF = spark.read.format("csv").option("header", "true").load(inTagsDataPath)
val inRatingsDF = spark.read.format("csv").option("header", "true").load(inRatingsDataPath)

// Collect tags for movies
val tagsDF = inTagsDF.
  withColumnRenamed("movieId", "movieIdTags").
  withColumn("tags_info", struct("userId", "tag", "timestamp")).
  groupBy("movieIdTags").
  agg(collect_list("tags_info").as("tags"))

val tagsSchema = tagsDF.schema(1).dataType
val emptyTag = udf(() => Seq.empty[Any],tagsSchema)

// Collect ratings for movies
val ratingsDF = inRatingsDF.
  withColumnRenamed("movieId", "movieIdRatings").
  withColumn("ratings_info", struct("userId", "rating", "timestamp")).
  groupBy("movieIdRatings").
  agg(collect_list("ratings_info").as("ratings"))

val ratingsSchema =ratingsDF.schema(1).dataType
val emptyRating = udf(() => Seq.empty[Any],ratingsSchema)

// Join movies, tags and ratings
val moviesDF = inMoviesDF.
  join(tagsDF, inMoviesDF.col("movieId") === tagsDF.col("movieIdTags"), "left").
  join(ratingsDF, inMoviesDF.col("movieId") === ratingsDF.col("movieIdRatings"), "left")

// Write result data
moviesDF.select(col("movieId"), col("title"), col("genres"), when(col("tags").isNull, emptyTag()).otherwise(col("tags")).as("tags"), when(col("ratings").isNull, emptyRating()).otherwise(col("ratings")).as("ratings")).write.format("json").save(outDataPath)