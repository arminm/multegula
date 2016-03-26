#!/bin/bash
node1=$(sed -n '1 p' ./dns)
scp -i ~/.ssh/lwhecser.pem -r ../src ubuntu@$node1:~/

node2=$(sed -n '2 p' ./dns)
scp -i ~/.ssh/lwhecser.pem -r ../src ubuntu@$node2:~/

node3=$(sed -n '3 p' ./dns)
scp -i ~/.ssh/lwhecser.pem -r ../src ubuntu@$node3:~/
