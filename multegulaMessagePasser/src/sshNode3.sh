#!/bin/bash
dns=$(sed -n '3 p' ./dns)
ssh -i ~/.ssh/lwhecser.pem ubuntu@$dns 
