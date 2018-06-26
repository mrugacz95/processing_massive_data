facts.groupBy("song_id").
    count.
    join(songs, facts("song_id") === songs("song_id")).
    select("song_long_id", "count").
    orderBy(desc("count")).
    show(10)