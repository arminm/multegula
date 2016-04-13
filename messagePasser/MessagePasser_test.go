package messagePasser

import "testing"

func TestIsMessageReady(t *testing.T) {
	timestamp := []int{1, 2, 3}
	message := Message{"", "", "", "", 0, []int{1, 3, 4}}
	sourceIndex := 1
	t.Log("Testing timestamp with 1 incremented value...")
	message.Timestamp = []int{1, 3, 3}
	if !isMessageReady(message, sourceIndex, &timestamp) {
		t.Errorf("Message should be ready!\nMessage Timestamp: %v\nLocal Timestamp: %v\n",
			message.Timestamp, timestamp)
	}

	t.Log("Testing timestamp with 2 incremented values...")
	message.Timestamp = []int{1, 3, 4}
	if isMessageReady(message, sourceIndex, &timestamp) {
		t.Errorf("Message should NOT be ready!\nMessage Timestamp: %v\nLocal Timestamp: %v\n",
			message.Timestamp, timestamp)
	}

	t.Log("Testing timestamp with 1 incremented value and 1 smaller value...")
	message.Timestamp = []int{1, 3, 4}
	if isMessageReady(message, sourceIndex, &timestamp) {
		t.Errorf("Message should NOT be ready!\nMessage Timestamp: %v\nLocal Timestamp: %v\n",
			message.Timestamp, timestamp)
	}

	t.Log("Testing timestamp with equal values")
	message.Timestamp = []int{1, 2, 3}
	if isMessageReady(message, sourceIndex, &timestamp) {
		t.Errorf("Message should NOT be ready!\nMessage Timestamp: %v\nLocal Timestamp: %v\n",
			message.Timestamp, timestamp)
	}

	t.Log("Testing timestamp with smaller values")
	message.Timestamp = []int{1, 1, 1}
	if isMessageReady(message, sourceIndex, &timestamp) {
		t.Errorf("Message should NOT be ready!\nMessage Timestamp: %v\nLocal Timestamp: %v\n",
			message.Timestamp, timestamp)
	}

	t.Log("Testing timestamp with larger values")
	message.Timestamp = []int{1, 7, 10}
	if isMessageReady(message, sourceIndex, &timestamp) {
		t.Errorf("Message should NOT be ready!\nMessage Timestamp: %v\nLocal Timestamp: %v\n",
			message.Timestamp, timestamp)
	}
}
