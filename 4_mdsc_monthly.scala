facts.select("date_id").
    join(date, date("date_id") === facts("date_id")).
    groupBy("month").
    agg(count("month") as "count").
    orderBy("month").
    show()