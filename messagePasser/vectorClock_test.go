package messagePasser

import "testing"

func TestGetNewTimestamp(t *testing.T) {
	testTimestamp := []int{2, 0, 1, 5, 12}
	expectedTimestamp := []int{2, 1, 1, 5, 12}
	newTimestamp := GetNewTimestamp(&testTimestamp, 1)
	if !CompareTimestampsSame(newTimestamp, &expectedTimestamp) || !CompareTimestampsSame(&testTimestamp, &expectedTimestamp) {
		t.Errorf("Failed to get new timestamp.\ntestTimestamp:%+v\nnewTimestamp:%+v\nexpected:%+v\n",
			testTimestamp, newTimestamp, expectedTimestamp)
	}
}

func TestUpdateTimestamp(t *testing.T) {
	testTimestamp := []int{2, 0, 1, 5, 12}
	newTimestamp := []int{3, 0, 0, 4, 20}
	expectedTimestamp := []int{3, 0, 1, 5, 20}
	UpdateTimestamp(&testTimestamp, &newTimestamp)
	if !CompareTimestampsSame(&testTimestamp, &expectedTimestamp) {
		t.Errorf("Failed to update timestamp.\ntestTimestamp:%+v\nnewTimestamp:%+v\nexpected:%+v\n",
			testTimestamp, newTimestamp, expectedTimestamp)
	}
}

func TestIncrementTimestamp(t *testing.T) {
	testTimestamp := []int{2, 0, 1, 5, 12}
	expectedTimestamp := []int{2, 1, 1, 5, 12}
	IncrementTimestamp(&testTimestamp, 1)
	if !CompareTimestampsSame(&testTimestamp, &expectedTimestamp) {
		t.Errorf("Failed to increment timestamp.\n")
	}
}

func TestCompareTimestampsSame(t *testing.T) {
	testTimestamp := []int{2, 0, 1, 5, 12}

	sameTimestamp := []int{2, 0, 1, 5, 12}
	if !CompareTimestampsSame(&testTimestamp, &sameTimestamp) {
		t.Errorf("Failed to compare with same timestamp.\ntestTimestamp:%+v\nCompared with:%+v\n",
			testTimestamp, sameTimestamp)
	}

	emptyTimestamp := []int{}
	if CompareTimestampsSame(&testTimestamp, &emptyTimestamp) {
		t.Errorf("Failed to compare with empty timestamp.\ntestTimestamp:%+v\nCompared with:%+v\n",
			testTimestamp, emptyTimestamp)
	}
}

func TestCompareTimestamps(t *testing.T) {
	testTimestamp := []int{2, 0, 1, 5, 12}

	earlierTimestamp := []int{2, 0, 1, 5, 11}
	if earlier, later, _ := CompareTimestamps(&testTimestamp, &earlierTimestamp); !CompareTimestampsSame(&earlierTimestamp, earlier) {
		t.Errorf("Failed to get earlier timestamp.\ntestTimestamp:%+v\nCompared with:%+v\nEarlier: %+v\n",
			testTimestamp, earlierTimestamp, *earlier)
	} else if !CompareTimestampsSame(&testTimestamp, later) {
		t.Errorf("Failed to get later timestamp.\ntestTimestamp:%+v\nCompared with:%+v\nLater: %+v\n",
			testTimestamp, earlierTimestamp, *later)
	}

	laterTimestamp := []int{2, 0, 1, 6, 13}
	if earlier, later, _ := CompareTimestamps(&testTimestamp, &laterTimestamp); !CompareTimestampsSame(&testTimestamp, earlier) {
		t.Errorf("Failed to get earlier timestamp.\ntestTimestamp:%+v\nCompared with:%+v\nEarlier: %+v\n",
			testTimestamp, laterTimestamp, *earlier)
	} else if !CompareTimestampsSame(&laterTimestamp, later) {
		t.Errorf("Failed to get later timestamp.\ntestTimestamp:%+v\nCompared with:%+v\nLater: %+v\n",
			testTimestamp, laterTimestamp, *later)
	}

	concurrentTimestamp := []int{2, 0, 1, 4, 13}
	if _, _, err := CompareTimestamps(&testTimestamp, &concurrentTimestamp); err == nil {
		t.Errorf("Failed to detect concurrent timestamps.\ntestTimestamp:%+v\nCompared with:%+v\n",
			testTimestamp, concurrentTimestamp)
	}

	malformedTimestamp := []int{1, 2}
	if _, _, err := CompareTimestamps(&testTimestamp, &malformedTimestamp); err == nil {
		t.Errorf("Failed to detect concurrent timestamps.\ntestTimestamp:%+v\nCompared with:%+v\n",
			testTimestamp, malformedTimestamp)
	}
}
