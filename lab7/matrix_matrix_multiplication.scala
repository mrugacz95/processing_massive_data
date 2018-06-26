val M = sc.textFile("matrix_multip/M.txt").map( x => {  val t =x.split(" "); (t(0).toInt, t(1).toInt, t(2).toInt)}).
    flatMap( x => {(1 to 10).map{k => ((x._1,k),("M", x._2, x._3))}})
val N = sc.textFile("matrix_multip/N.txt").map( x => {  val t =x.split(" "); (t(0).toInt, t(1).toInt, t(2).toInt)}).
    flatMap( x => {(1 to 10).map{i => ((i,x._2),("N", x._1, x._3))}})
M.join(N).
    mapValues(x => List(x._1,x._2)).
    reduceByKey(_ ++ _).
    mapValues(x => {
        val m:List[(String,Int,Int)] = x.filter(p => p._1 == "M").sortWith((f,s) => f._2 < s._2);
        val n:List[(String,Int,Int)] = x.filter(p => p._1 == "N").sortWith((f,s) => f._2 < s._2);
        (m zip n).map{case (f,s) => (f._3*s._3)}.sum / 2
    }).
    take(20)
val M = sc.textFile("matrix_multip/M.txt").map( x => {  val t =x.split(" "); (t(0).toInt, t(1).toInt, t(2).toInt)}).
    map( x => (x._2,(x._1, x._3)))
val N = sc.textFile("matrix_multip/N.txt").map( x => {  val t =x.split(" "); (t(0).toInt, t(1).toInt, t(2).toInt)}).
    map( x => (x._1,(x._2, x._3)))
M.join(N).
    map({ case (_, ((i, v), (k, w))) => ((i, k), (v * w)) }).
    reduceByKey(_ + _).
    take(20)