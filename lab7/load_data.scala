val songs=spark.read.
    option("delimiter",";").
    csv("msdc/songs.csv").
    toDF("song_id","track_long_id","song_long_id","artist_id")
val facts=spark.read.
    option("delimiter",";").
    csv("msdc/listen.csv").
    toDF("user_id","song_id","date_id","artist_id")
val date = spark.read.
    option("delimiter", ";").
    csv("msdc/date.csv").
    toDF("date_id", "month", "year")
val song_artist = spark.read.
    option("delimiter", ";").
    csv("msdc/song_artist.csv").
    toDF("song_id", "artist_id")
val artist = spark.read.
    option("delimiter", ";").
    csv("msdc/artist.csv").
    toDF("artist_id", "artist")
val users = spark.read.
    option("delimiter", ";").
    csv("msdc/users.csv").
    toDF("user_id", "user_long_id")