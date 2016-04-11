package messagePasser

import "fmt"

/*
 * initializes a new timestamp by incrementing and copying the current timestamp
 */
func GetNewTimestamp(currentTimestamp *[]int, localIndex int, seqNum int) *[]int {
	newTimestamp := make([]int, len(*currentTimestamp))
	copy(newTimestamp, *currentTimestamp)
	newTimestamp[localIndex] = seqNum
	return &newTimestamp
}

/*
 * updates a vector timestamp using a new timestamp.
 */
func UpdateTimestamp(currentTimestamp *[]int, newTimestamp *[]int) error {
	if len(*currentTimestamp) != len(*newTimestamp) {
		return fmt.Errorf("Can't update vector with a new vector of different length (%d != %d)\n",
			len(*currentTimestamp), len(*newTimestamp))
	}
	for i, value := range *currentTimestamp {
		if value < (*newTimestamp)[i] {
			(*currentTimestamp)[i] = (*newTimestamp)[i]
		}
	}

	return nil
}

/*
 * increments a timestamp at a certain local index for the local node
 */
func IncrementTimestamp(v1 *[]int, localIndex int) {
	if localIndex >= 0 && localIndex < len(*v1) {
		(*v1)[localIndex] = (*v1)[localIndex] + 1
	}
}

/*
 * compares two timestamps and returns the earlier and later timestamps.
 * will return an error if two timestamps are concurrent or can't be compared.
 */
func CompareTimestamps(v1 *[]int, v2 *[]int) (earlier *[]int, later *[]int, err error) {
	if len(*v1) != len(*v2) {
		return earlier, later, fmt.Errorf("Can't compare vectors with different lengths (%d != %d)\n", len(*v1), len(*v2))
	}
	if CompareTimestampsLE(v1, v2) {
		earlier = v1
		later = v2
	} else if CompareTimestampsLE(v2, v1) {
		earlier = v2
		later = v1
	} else {
		err = fmt.Errorf("Timestamps are concurrent.\nv1:%+v\nv2%+v\n", *v1, *v2)
	}
	return earlier, later, err
}

/*
 * compares two timestamps to detect if the first timestamp happens before or
 * at the same time as the second timestamp
 */
func CompareTimestampsLE(v1 *[]int, v2 *[]int) bool {
	if len(*v1) != len(*v2) {
		return false
	}
	for i, val := range *v1 {
		if val > (*v2)[i] {
			return false
		}
	}
	return true
}

/*
 * compares two timestamps to check for equality.
 */
func CompareTimestampsSame(v1 *[]int, v2 *[]int) bool {
	if len(*v1) != len(*v2) {
		return false
	}
	for i, value := range *v1 {
		if value != (*v2)[i] {
			return false
		}
	}
	return true
}
