package messagePasser

func Push(queue *[]Message, obj Message) {
	*queue = append(*queue, obj)
}

func Pop(queue *[]Message, obj Message) Message {
	return obj
}

func Insert(queue []Message, obj Message, index int) {

}
