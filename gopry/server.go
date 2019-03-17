package main

import (
	"fmt"
	"net"
	"os"
	"time"
)

const (
	CONN_HOST = "localhost"
	CONN_PORT = "3333"
	CONN_TYPE = "tcp"
)

func main() {
	l, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		fmt.Println("Error listening: ", err.Error())
		os.Exit(1)
	}
	defer l.Close()
	fmt.Println("Listening on " + CONN_HOST + ":" + CONN_PORT)
	openConnChannel := make(chan net.Conn, 10)
	go func() {
		for {
			conn, err:= l.Accept()
			if err != nil {
				fmt.Println("Error accepting: ", err.Error())
				os.Exit(1)
			}
			fmt.Println("Accepted")
			openConnChannel <- conn
		}
	}()
	for {
		select {
			case conn := <-openConnChannel:
				go handleRequest(conn)
		}
	}
}
func handleRequest(conn net.Conn) {
	messageChannel := make(chan string,1)
	go handleRequestRead(conn, messageChannel)
	select {
		case message := <-messageChannel:
			fmt.Println("Reading message")
			fmt.Println(message)
			conn.Write([]byte("Message received."))
		case <-time.After(10 * time.Second):
			fmt.Println("Timeout")
	                conn.Write([]byte("Can't handle message."))
	}
	fmt.Println("Closing connection")
	conn.Close()

}
func handleRequestRead(conn net.Conn, messageChannel chan string) {
            buf := make([]byte, 1024)
	    reqLen, err := conn.Read(buf)
	    if err != nil {
		fmt.Println("Error reading: ", err.Error())
	    }else {
		    messageChannel <- string(buf[:reqLen])
		}
}
