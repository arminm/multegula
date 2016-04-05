package messagePasser

func Push(queue *[]Message, message Message) {
	*queue = append(*queue, message)
}

func Pop(queue *[]Message) Message {
	message := (*queue)[0]
	*queue = (*queue)[1:]
	return message
}

func Delete(queue *[]Message, index int) {
	*queue = append((*queue)[:index], (*queue)[index+1:]...)
}

func Insert(queue *[]Message, message Message, index int) *[]Message {
	newQueue := make([]Message, len(*queue)+1)
	copy(newQueue[:index], (*queue)[:index])
	copy(newQueue[index+1:], (*queue)[index:])
	newQueue[index] = message
	return &newQueue
}
