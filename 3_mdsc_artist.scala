facts.select("artist_id").
    groupBy("artist_id").
    agg(count("artist_id") as "count").
    orderBy(desc("count")).
    limit(10).
    join(artist, facts("artist_id") === artist("artist_id")).
    select("artist", "count").
    orderBy(desc("count")).
    show(10)