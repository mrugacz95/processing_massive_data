sc.textFile("all-shakespeare").flatMap(_.split(" ")).map(x => x.trim()).map(x => (x,1)).reduceByKey(_+_).sortBy(-_._2).saveAsTextFile("wordcount")