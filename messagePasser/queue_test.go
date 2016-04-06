package messagePasser

import "testing"

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

func TestPop(t *testing.T) {
	msg0 := Message{"Lunwen", "Armin", "Hi Armin!", "Regular", 1}
	msg1 := Message{"Armin", "Lunwen", "Hi Lunwen!", "Regular", 1}
	msg2 := Message{"Daniel", "", "Hi All!", "Multicast", 1}
	queue := make([]Message, 3, 5)
	queue[0], queue[1], queue[2] = msg0, msg1, msg2

	result := Pop(&queue)
	if result != msg0 {
		t.Errorf("Message was not popped.\nQueue:%+v\nResult:%+v", queue, result)
	}
}

func TestDelete(t *testing.T) {
	msg0 := Message{"Lunwen", "Armin", "Hi Armin!", "Regular", 1}
	msg1 := Message{"Armin", "Lunwen", "Hi Lunwen!", "Regular", 1}
	msg2 := Message{"Daniel", "", "Hi All!", "Multicast", 1}
	queue := make([]Message, 3, 5)
	queue[0], queue[1], queue[2] = msg0, msg1, msg2

	Delete(&queue, 1)
	if queue[1] == msg1 {
		t.Errorf("Message was not deleted.\nQueue:%+v\nMessage:%+v", queue, msg1)
	}
}

func TestInsert(t *testing.T) {
	msg0 := Message{"Lunwen", "Armin", "Hi Armin!", "Regular", 1}
	msg1 := Message{"Armin", "Lunwen", "Hi Lunwen!", "Regular", 1}
	msg2 := Message{"Daniel", "", "Hi All!", "Multicast", 1}
	msg3 := Message{"Garrett", "", "Heeey!!", "Multicast", 1}

	queue := make([]Message, 1, 4)
	queue[0] = msg0

	queue = *(Insert(&queue, msg1, 0))
	if queue[0] != msg1 {
		t.Errorf("Message was not inserted at beginning.\nQueue:%+v\nMessage:%+v", queue, msg1)
	}

	queue = *(Insert(&queue, msg2, 1))
	if queue[1] != msg2 {
		t.Errorf("Message was not inserted in middle.\nQueue:%+v\nMessage:%+v", queue, msg2)
	}

	queue = *(Insert(&queue, msg3, 3))
	if queue[3] != msg3 {
		t.Errorf("Message was not inserted at end of queue.\nQueue:%+v\nMessage:%+v", queue, msg3)
	}

}
