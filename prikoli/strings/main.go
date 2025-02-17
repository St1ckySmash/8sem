package main

import (
	"fmt"
)

func main() {
	s := "assaldjflkasjdf;lkj"
	rune_ := []rune(s)[4]
	fmt.Println(string(rune_))
}
