package main

import (
	"errors"
	"fmt"
)

type Node[T any] struct {
	val  T
	next *Node[T]
}

type List[T any] struct {
	head *Node[T]
	tail *Node[T]
}

func NewList[T any](v T) *List[T] {
	node := &Node[T]{
		val:  v,
		next: nil,
	}
	return &List[T]{
		head: node,
		tail: node,
	}
}

func (l *List[T]) Add(v T) {
	l.tail.next = &Node[T]{
		val: v,
	}
	l.tail = l.tail.next
}

func (l *List[T]) LastVal() T {
	return l.tail.val
}

func (l *List[T]) Length() int {
	count := 0
	this := l.head
	for {
		count += 1
		if this.next == nil {
			return count
		}
		this = this.next

	}
}

func (l *List[T]) GetVal(ind int) (T, error) {
	i := 0
	this := l.head
	for {
		if i == ind {
			return this.val, nil
		}
		if this.next == nil {
			var zero T
			return zero, errors.New("end of list")
		}
		i += 1
		this = this.next

	}
}
func main() {
	list := NewList(2)
	list.Add(3)
	list.Add(1)
	list.Add(5)
	list.Add(4)
	fmt.Println(list.Length())
	fmt.Println(list.LastVal())
	fmt.Println(list.GetVal(0))
	fmt.Println(list.GetVal(1))
	fmt.Println(list.GetVal(2))
	fmt.Println(list.GetVal(3))
	fmt.Println(list.GetVal(4))
	fmt.Println(list.GetVal(5))
	fmt.Println(list.GetVal(6))

}
