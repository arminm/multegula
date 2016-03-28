package messagePasser

import "testing"

func TestEncodeMessage(t *testing.T) {
  t.Log("Testing encodeMessage...")
  var message Message = Message{"Source","Destination","Some Content!","Some Kind"}
  var expectedResult string = "Source##Destination##Some Content!##Some Kind"

  result := encodeMessage(message)
  if result != expectedResult {
    t.Errorf("Expected: %v\nResult: %v", expectedResult, result)
  }
}

func TestDecodeMessage(t *testing.T) {
  var encodedMessage string = "Source##Destination##Some Content!##Some Kind"
  var expectedResult Message = Message{"Source","Destination","Some Content!","Some Kind"}

  result := decodeMessage(encodedMessage)
  if result != expectedResult {
    t.Errorf("Expected: %+v\nResult: %+v", expectedResult, result)
  }
}
