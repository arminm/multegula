package io

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"os"

	"github.com/arminm/multegula/messagePasser"
)

/*
* Stores nodes data to a file
 */
func StoreNodes(fname string, peers *[]messagePasser.Node) error {
	b := new(bytes.Buffer)
	enc := gob.NewEncoder(b)
	err := enc.Encode(peers)
	if err != nil {
		return err
	}

	fh, eopen := os.OpenFile(fname, os.O_CREATE|os.O_WRONLY, 0666)
	defer fh.Close()
	if eopen != nil {
		return eopen
	}
	n, e := fh.Write(b.Bytes())
	if e != nil {
		return e
	}
	fmt.Fprintf(os.Stderr, "%d bytes successfully written to file\n", n)
	fh.Sync()
	return nil
}

/*
* Stores time data to a file
 */
func StoreTime(fname string, timestamp int64) error {
	b := new(bytes.Buffer)
	enc := gob.NewEncoder(b)
	err := enc.Encode(timestamp)
	if err != nil {
		return err
	}
	fh, eopen := os.OpenFile(fname, os.O_CREATE|os.O_WRONLY, 0666)
	defer fh.Close()
	if eopen != nil {
		return eopen
	}
	n, e := fh.Write(b.Bytes())
	if e != nil {
		return e
	}
	fmt.Fprintf(os.Stderr, "%d bytes successfully written to file\n", n)
	fh.Sync()
	return nil
}

/*
* Reads nodes data from a file
 */
func LoadNodes(fname string) *[]messagePasser.Node {
	fh, err := os.Open(fname)
	if err != nil {
		return nil
	}
	p := make([]messagePasser.Node, 3)
	dec := gob.NewDecoder(fh)
	err = dec.Decode(&p)
	if err != nil {
		return nil
	}
	return &p
}

/*
* Reads time data from a file
 */
func LoadTime(fname string) (int64, error) {
	fh, err := os.Open(fname)
	if err != nil {
		return -1, err
	}
	var t int64
	dec := gob.NewDecoder(fh)
	err = dec.Decode(&t)
	if err != nil {
		return -1, err
	}
	return t, nil
}
