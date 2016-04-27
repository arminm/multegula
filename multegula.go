////////////////////////////////////////////////////////////
//Multegula - multegula.go
//Main Go Package for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
	"flag"
	"fmt"
	"reflect"
	"sort"
	"strconv"
	"strings"

	"github.com/arminm/multegula/bootstrapClient"
	"github.com/arminm/multegula/bridges"
	"github.com/arminm/multegula/bullySelection"
	"github.com/arminm/multegula/consensus"
	"github.com/arminm/multegula/defs"
	"github.com/arminm/multegula/messagePasser"
)

/*
 * This is the sendChannel for message dispatcher.
 * Any components like UI or bully algorithm will
 * put messages into this channel if they want to
 * send message out. Message dispatcher will get
 * messages out from this channel and send them
 * to messagePasser
 */
var sendChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

/*
 * keeping track of the proposal checks
 */

var propChecksMap map[string]*consensus.PropCheck = make(map[string]*consensus.PropCheck)

/*
 * put message into sendChannel
 * @param message - message to be put into sendChannel
 */
func putMessageIntoSendChannel(message messagePasser.Message) {
	sendChannel <- message
}

/*
 * get the operation, send or receive
 * @return if send, return 1; otherwise return 0
 **/
func getOperation() int {
	var operation string
	for {
		fmt.Println("Send(s) / Receive(r) / Multicast (m): ")
		fmt.Scanf("%s", &operation)
		switch operation {
		case "s":
			return 0
		case "r":
			return 1
		case "m":
			return 2
		default:
			fmt.Printf("'%v' is Invalid. Please select a valid operation.", operation)
		}
	}
}

/*
 * get destination name
 * @param nodes
 *        the available nodes to contact
 *
 * @return destination name string
 **/
func getDest(nodes []messagePasser.Node) string {
	fmt.Println("To: (ex. lunwen OR 1)")
	var destName string
	fmt.Scanf("%v", &destName)
	// Check if input is an ID
	id, err := strconv.Atoi(destName)
	if err == nil && id >= 0 && id < len(nodes) {
		return nodes[id].Name
	}
	// else input must be a name
	var destNode messagePasser.Node
	for len(destName) > 0 {
		_, destNode, err = messagePasser.FindNodeByName(nodes, destName)
		if err == nil {
			break
		}
		fmt.Printf("Couldn't find '%v', please try again:\n", destName)
		fmt.Scanf("%v", &destName)
	}

	return destNode.Name
}

/*
 * get string from stdin
 * @param stringType
 *        the type of string: message content or message kind
 *
 * @return string got from stdin
 **/
func getString(stringType string) string {
	fmt.Println("Please input " + stringType + ":")
	var res string
	fmt.Scanf("%s", &res)
	return res
}

/*
 * Prompts the user for the configuration file's name
 * @return configuration file's name string
 */
func getConfigName() string {
	var configName string
	fmt.Println("What's the config file's name? (ex. config)")
	fmt.Scanf("%s", &configName)
	if len(configName) == 0 {
		configName = "config" // default name
	}
	return configName
}

/*
 * Prompts the user for the local Node's name
 * @return local Node's name string
 */
func getLocalName() string {
	var localName string
	fmt.Println("Who are you? (ex. armin)")
	fmt.Scanf("%s", &localName)
	if len(localName) == 0 {
		localName = "unknown" // default name
	}
	return localName
}

/*
 * prompts the user and builds a message
 */
func getMessage(nodes []messagePasser.Node, localNodeName string) messagePasser.Message {
	dest := getDest(nodes)
	kind := getString("message kind")
	content := getString("message content")
	return messagePasser.Message{Source: localNodeName, Destination: dest, Content: content, Kind: kind}
}

/*
 * retreives local name from the UI
 */
func uiGetLocalName() (localName string) {
	for {
		message := bridges.ReceiveFromPyBridge()
		if message.Kind == defs.MSG_MYNAME {
			localName = message.Content
			break
		}
	}
	return localName
}

/*
 * retreives game type from the UI
 */
func uiGetGameType() (gameType string) {
	for {
		message := bridges.ReceiveFromPyBridge()
		if message.Kind == defs.MSG_GAME_TYPE {
			gameType = message.Content
			break
		}
	}
	return gameType
}

/*
 * sets the orientation of the players to alphabetical
 */
func uiSetCompetitorLocation(myName string, peers *[]messagePasser.Node) {
	var toSend messagePasser.Message
	var nodeNames = []string{}

	// loop through all nodes and pull out names
	for _, node := range *peers {
		nodeNames = append(nodeNames, node.Name)
	}

	// sort and get length
	sort.Strings(nodeNames)
	length := len(nodeNames)

	// create content of message
	content := fmt.Sprintf("%d", length)
	for _, name := range nodeNames {
		content = fmt.Sprintf("%v%v%v", content, defs.PAYLOAD_DELIMITER, name)
	}

	// create message and send message
	toSend.Source = myName
	toSend.Destination = myName
	toSend.Kind = defs.MSG_PLAYER_LOC
	toSend.Content = content
	bridges.SendToPyBridge(toSend)
}

/* wait for incoming messages from the UI */
func PyBridgeReceiver() {
	for {
		message := bridges.ReceiveFromPyBridge()
		switch message.Kind {
		case defs.MSG_CON_REQ:
			valueType := strings.Split(message.Content, "|")[0]
			consensus.Propose(message.Content, valueType)
		case defs.MSG_CON_REPLY:
			valueType := strings.Split(message.Content, "|")[0]
			propCheck := propChecksMap[valueType]
			(*propCheck.Callback)(message.Content)
			delete(propChecksMap, valueType)
		default:
			go putMessageIntoSendChannel(message)
		}
	}
}

/* wait for incoming messages from the bully algorithm */
func BullyReceiver() {
	for {
		message := bullySelection.GetMessageFromSendChannel()
		go putMessageIntoSendChannel(message)
	}
}

/*
 * get unicorn update message from bullySelection,
 * send unicorn update message to ui and consensus algorithm
 */
//TODO add code to send unicorn update message to consensus algorithm
func UnicornReciever() {
	for {
		unicornUpdateMessage := bullySelection.GetUnicornUpdate()
		go putMessageIntoSendChannel(unicornUpdateMessage)
	}
}

/* wait for incoming messages from consensus algorithm */
func ConsensusReceiverRoutine() {
	for {
		message := consensus.SendMessage()
		go putMessageIntoSendChannel(*message)
	}
}

/*
 * Routine to check proposals for a local value and respond
 */
func ConsensusCheckReceiverRoutine() {
	for {
		propCheck := consensus.ProposalCheck()
		propChecksMap[propCheck.Prop.Type] = propCheck
		bridges.SendToPyBridge(messagePasser.Message{
			Source:      messagePasser.LocalNode.Name,
			Destination: messagePasser.LocalNode.Name,
			Kind:        defs.MSG_CON_CHECK,
			Content:     propCheck.Prop.Value,
		})
	}
}

/*
 * Routine to commit proposals that have reached consensus
 */
func ConsensusReachedRoutine() {
	for {
		proposal := consensus.ProposalToCommit()
		commitMessage := messagePasser.Message{
			Source:      messagePasser.LocalNode.Name,
			Destination: messagePasser.LocalNode.Name,
			Kind:        defs.MSG_CON_COMMIT,
			Content:     proposal.Value,
		}
		bridges.SendToPyBridge(commitMessage)
	}
}

/* receive message from messagePasser and route to correct location */
func inboundDispatcher() {
	for {
		// get message from MessagePasser
		message := messagePasser.Receive()

		// Based on the type of message, determine where it needs routed
		switch message.Kind {

		// UI Messages
		case defs.MSG_BALL_DEFLECTED:
			fallthrough
		case defs.MSG_BALL_MISSED:
			fallthrough
		case defs.MSG_BLOCK_BROKEN:
			fallthrough
		case defs.MSG_CON_COMMIT:
			fallthrough
		case defs.MSG_DEAD_NODE:
			fallthrough
		case defs.MSG_PADDLE_DIR:
			fallthrough
		case defs.MSG_PAUSE_UPDATE:
			fallthrough
		case defs.MSG_START_PLAY:
			fallthrough
		case defs.MSG_SYNC_ERROR:
			fallthrough
		case defs.MSG_UNICORN:
			initConsensus(message)
			bridges.SendToPyBridge(message)

		// election messages
		case defs.MSG_BULLY_ELECTION:
			fallthrough
		case defs.MSG_BULLY_ANSWER:
			fallthrough
		case defs.MSG_BULLY_UNICORN:
			initConsensus(message)
			fallthrough
		case defs.MSG_BULLY_ARE_YOU_ALIVE:
			fallthrough
		case defs.MSG_BULLY_IAM_ALIVE:
			bullySelection.PutMessageToReceiveChannel(message)

		// consensus messages
		case defs.CONSENSUS_ACCEPT_KIND:
			fallthrough
		case defs.CONSENSUS_REJECT_KIND:
			fallthrough
		case defs.CONSENSUS_PROPOSE_KIND:
			fallthrough
		case defs.CONSENSUS_COMMIT_KIND:
			consensus.ReceiveMessage(message)
		default:
			fmt.Printf("inboundDispatcher couldn't recognize message: %+v\n", message)
		}
	}
}

/* Handles all outbound messages  */
func outboundDispatcher() {
	for {
		// get message from the send channel
		message := <-sendChannel
		// based on it's destination, determine which messagePasser
		//	routine is appropriate
		if message.Destination == defs.MULTICAST_DEST {
			messagePasser.Multicast(&message)
		} else {
			messagePasser.Send(message)
		}
	}
}

/*
 * parses main arguments passed in through command-line
 */
func parseMainArguments(args []string) string {
	var localNodeName string
	if len(args) > 0 {
		localNodeName = args[1]
	} else {
		localNodeName = getLocalName()
	}
	fmt.Println("Local Node Name:", localNodeName)
	return localNodeName
}

/*
 * Inits consensus when we receive a unicorn message
 */
func initConsensus(message messagePasser.Message) {
	nodeIndex, node, err := messagePasser.FindNodeByName(messagePasser.PeerNodes, message.Content)
	if err == nil {
		peers := append(messagePasser.PeerNodes[:nodeIndex], messagePasser.PeerNodes[nodeIndex+1:]...)
		consensus.InitConsensus(node, peers, messagePasser.LocalNode.Name)
		go ConsensusReceiverRoutine()
		go ConsensusCheckReceiverRoutine()
		go ConsensusReachedRoutine()
		fmt.Println("Consensus initialized by leader:", node.Name)
	}
}

/* the Main function of the Multegula application */
func main() {
	testFlag := flag.Bool("test", false, "Test Mode Flag")
	bootstrapTestFlag := flag.Bool("bt", false, "Bootstrap Test Mode Flag")
	consensusTestFlag := flag.Bool("ct", false, "Consensus Test Mode Flag")
	uiPortFlag := flag.Int("uiport", defs.DEFAULT_UI_PORT, "Local port number for Python-Go bridge.")
	gamePortFlag := flag.Int("gameport", defs.DEFAULT_GAME_PORT, "Local port number for MessagePasser.")
	flag.Parse()
	// Read command-line arguments and prompt the user if not provided
	args := flag.Args()

	// nodes used for testing purposes only
	nodes := []messagePasser.Node{messagePasser.Node{Name: "armin", IP: "127.0.0.1", Port: 10011}, messagePasser.Node{Name: "garrett", IP: "127.0.0.1", Port: 10012}, messagePasser.Node{Name: "lunwen", IP: "127.0.0.1", Port: 10013}, messagePasser.Node{Name: "daniel", IP: "127.0.0.1", Port: 10014}}
	// nodes := []messagePasser.Node{messagePasser.Node{Name: "armin", IP: "50.131.53.106", Port: 11111}, messagePasser.Node{Name: "garrett", IP: "71.199.96.75", Port: 44444}, messagePasser.Node{Name: "daniel", IP: "50.131.53.106", Port: 22222}, messagePasser.Node{Name: "lunwen", IP: "71.199.96.75", Port: 33333}}

	// for testing consensus
	if *consensusTestFlag {
		localName := getLocalName()
		messagePasser.InitMessagePasser(nodes, localName)
		go outboundDispatcher()
		go inboundDispatcher()
		leader := nodes[0]
		consensus.InitConsensus(leader, nodes[1:], localName)
		go ConsensusReceiverRoutine()
		go ConsensusCheckReceiverRoutine()
		go ConsensusReachedRoutine()

		var proposalValue string
		for {
			if localName == leader.Name {
				fmt.Println("Hit enter to propose.")
				fmt.Scanf("%s", &proposalValue)
				consensus.Propose(proposalValue, "test")
			}
		}
	}

	// for testing the bootstrapping
	if *bootstrapTestFlag {
		localName := getLocalName()
		_, localNode, _ := messagePasser.FindNodeByName(nodes, localName)
		fmt.Println("Contacting the bootstrap server...")
		peers, err := bootstrapClient.GetNodes(localNode)
		if err != nil {
			fmt.Println("Got error:", err)
		} else {
			fmt.Printf("Got peers: %+v\n", peers)
		}
		return
	}

	if *testFlag {
		localNodeName := parseMainArguments(args)
		localNode := messagePasser.Node{Name: localNodeName, IP: "127.0.0.1", Port: *gamePortFlag}
		peers, err := bootstrapClient.GetNodes(localNode)
		if err != nil {
			fmt.Println("Couldn't get peers:", err)
			panic(err)
		}
		*peers = append(*peers, localNode)
		fmt.Print("--------------------------------\n")
		fmt.Println("Available Nodes:")
		for id, node := range *peers {
			fmt.Printf("  ID:%d – %+v\n", id, node)
		}
		fmt.Println("Initing with localName:", localNodeName)
		messagePasser.InitMessagePasser(*peers, localNodeName)

		/* start a receiveRoutine to be able to use nonBlockingReceive */
		go receiveRoutine()

		fmt.Println("Please select the operation you want to do:")
		for {
			fmt.Println("Getting operation")
			operation := getOperation()
			if operation == 0 {
				message := getMessage(nodes, localNodeName)
				messagePasser.Send(message)
			} else if operation == 1 {
				var message messagePasser.Message = nonBlockingReceive()
				if (reflect.DeepEqual(message, messagePasser.Message{})) {
					fmt.Print("No messages received.\n\n")
				} else {
					fmt.Printf("Received: %+v\n\n", message)
				}
			} else if operation == 2 {
				message := getMessage(nodes, localNodeName)
				messagePasser.Multicast(&message)
				fmt.Println("Did multicast")
			} else {
				fmt.Println("Operation not recognized. Please try again.")
			}
		}
	}

	/**** THIS IS LIKE ACTUAL GAMEPLAY ***/
	// initialize communication with the UI
	fmt.Printf("Port is:%d\n", *uiPortFlag)
	bridges.InitPyBridge(*uiPortFlag)

	// get the localname
	localNodeName := uiGetLocalName()
	fmt.Println("My name is:", localNodeName)

	// determine the game type (multi or single player)
	gameType := uiGetGameType()

	if gameType == defs.GAME_TYPE_MULTI {
		// get fellow players
		localNode := messagePasser.Node{Name: localNodeName, IP: "127.0.0.1", Port: *gamePortFlag}
		peers, err := bootstrapClient.GetNodes(localNode)
		if err != nil {
			fmt.Println("Couldn't get peers:", err)
			panic(err)
		}
		*peers = append(*peers, localNode)

		// set competitor location
		uiSetCompetitorLocation(localNode.Name, peers)

		// initialize message passer
		messagePasser.InitMessagePasser(*peers, localNodeName)
		fmt.Println(localNodeName, "made message passer.")

		// initialize elections
		go bullySelection.InitBullySelection(*peers, localNodeName)
		go UnicornReciever()

		/* start the routine waiting for messages coming from UI */
		go PyBridgeReceiver()
		go BullyReceiver()
		go inboundDispatcher()
		outboundDispatcher()
	}

}

/* testing functions */
var receiveQueue = []messagePasser.Message{}

func receiveRoutine() {
	for {
		messagePasser.Push(&receiveQueue, messagePasser.Receive())
	}
}

func nonBlockingReceive() messagePasser.Message {
	return messagePasser.Pop(&receiveQueue)
}
