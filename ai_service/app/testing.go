//package main
//
//import "fmt"
//
//func main() {
//	var x float32 = 10.0 / 6
//	var y int = 10 % 3
//	fmt.Println(x)
//	fmt.Println(y)
//}
//
//package main
//
//import "fmt"
//
//func main() {
//	var x int
//	var h int
//	var m int
//	fmt.Scan(&x)
//	h = x / 30
//	m = 2 * (x % 30)
//	fmt.Println("It is", h, "hours", m, "minutes.")
//}

//package main
//
//import (
//	"fmt"
//	"math"
//)
//
//func main() {
//	x := 2
//	n := 3
//	lim := 10
//	if res := math.Pow(float64(x), float64(n)); res < float64(lim) {
//		fmt.Printf("Результат: %.2f меньше лимита\n", res)
//	}
//}

//package main
//
//import "fmt"
//
//func main() {
//	var year uint32
//	fmt.Scan(&year)
//	if year%400 == 0 || year%4 == 0 && year%100 != 0 {
//		fmt.Println("YES")
//	} else {
//		fmt.Println("NO")
//	}
//}

package main

import "fmt"

func main() {
	var n uint16
	for fmt.Scan(&n); n <= 100; fmt.Scan(&n) {
		if n >= 10 {
			fmt.Println(n)
		}
	}
}
