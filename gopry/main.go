package main

import (
	"fmt"
)

type Node struct {
	value string
	child *Node
}

// Recursive string representation
func (node Node) String() string{
	result := ""
	for node.child != nil{
		result += node.value
		node = *node.child
	}
	result += node.value
	return result
}
func main() {
	a := Node{"h", nil}
	b := Node{"a", nil}
	a.child = &b
	fmt.Println(a)
}
