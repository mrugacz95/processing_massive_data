facts.select("song_id", "user_id", "artist_id").
    join(artist.filter(artist("artist")==="Queen").select("artist_id"),
         facts("artist_id") === artist("artist_id")).
    select("user_id", "song_id").
    groupBy("song_id").
    agg(countDistinct("user_id") as "listeners_count").
    orderBy(desc("listeners_count")).
    limit(3).
    select("song_id").
    join(facts.select("song_id", "user_id") as "facts2", facts("song_id") === $"facts2.song_id", "right").
    groupBy("user_id").
    agg(countDistinct(facts("song_id")) as "count").
    filter($"count" === 3).
    select($"facts2.user_id").
    join(users, users("user_id") === $"facts2.user_id").
    select("user_long_id").
    orderBy("user_long_id").
    show()
