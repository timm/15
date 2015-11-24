
//object HelloWorld {
  //   def main(args: Array[String]) {
  //     val start = System.currentTimeMillis
  //     // problem code here
  //     println("Hello, world!")
  //     val elapsed = System.currentTimeMillis - start
  //     println(s"Elapsed: $elapsed ms")
 
  //   }
  // }

//object Test {
//   def main(args: Array[String]) {
//      println("Hello\tWorld\n\n" );
//   }
//} 

def show(s: String) { println(s) }

def hello() {
  show("Hello, world!!!")
}
def factorial(x: BigInt): BigInt  = if (x == 0) 1 else x * factorial(x - 1)

print(factorial(30) )


var capital = Map("US" -> "Washington","France" -> "Paris")
capital += ("Japan" -> "Tokyo")
println(capital("Japan"))

hello()
