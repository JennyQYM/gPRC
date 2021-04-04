# gPRC

## Purpose
Build a distributed bank transaction system that allows multiple customers to withdraw or deposit money from the multiple branches in the bank. 
In this system:
-	One customer only communicates with one corresponding branch which has the same id with customer
-	Each branch communicates with all the rest branches to transfer the balance changes requested by its customer and to main same amount of money replica
-	Each branch initializes with same amount of money
-	After customers’ actions (query, withdraw, deposit), each branch will eventually have the same balance amount

## Goal
-	Understand RPC mechanism 
-	Learn and utilize gPRC Python to build the bank transaction system
-	Setup .proto file
-	Utilize pb2_grpc.py and grpc.py file to setup server/client
-	Start multiple servers successfully using multiprocessing
-	Send request from client and receive message from server
-	Make sure balance replica in each branch is consistent eventually. 
