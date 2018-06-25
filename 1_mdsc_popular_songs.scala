facts.groupBy("song_id").
    count.
    join(songs, facts("song_id") === songs("song_id")).
    select("song", "count").
    orderBy(desc("count")).
    show(10)