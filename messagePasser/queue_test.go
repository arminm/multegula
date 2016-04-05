package messagePasser

import "testing"

// type Message struct {
// 	Source      string // the DNS name of sending node
// 	Destination string // the DNS name of receiving node
// 	Content     string // the Content of message
// 	Kind        string // the Kind of messages
// 	SeqNum      int
// }
func TestPush(t *testing.T) {
	msg0 := Message{"Lunwen", "Armin", "Hi Armin!", "Regular", 1}
	msg1 := Message{"Armin", "Lunwen", "Hi Lunwen!", "Regular", 1}
	queue := make([]Message, 2, 5)
	queue[0], queue[1] = msg0, msg1
	msg2 := Message{"Daniel", "", "Hi All!", "Multicast", 1}
	Push(&queue, msg2)
	if queue[2] != msg2 {
		t.Errorf("Message was not pushed to queue.\nQueue:%+v\nMessage:%v", queue, msg2)
	}
}
