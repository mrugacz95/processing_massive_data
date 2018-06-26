facts.select("user_id","song_id").
    groupBy("user_id").
    agg(countDistinct("song_id") as "count").
    orderBy(desc("count")).
    limit(10).
    join(users, users("user_id") === facts("user_id")).
    select("user_long_id","count").
    orderBy(desc("count")).
    show(10)