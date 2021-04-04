from concurrent import futures
import multiprocessing
import time
import json

from Branch import Branch
from Customer import Customer

import grpc
import bank_pb2
import bank_pb2_grpc

def init_input():
    """process input txt file"""
    branches = []
    customers = []
    processids = []

    f = open('input.txt')
    input = json.loads(f.read())
    f.close()
    for event in input:
        if event['type'] == 'customer':
            customers.append(event)
        if event['type'] == 'branch':
            branches.append(event)
            processids.append(event['id'])

    return branches, customers, processids

def start_server(id, balance, branches):
    """start one server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bank_pb2_grpc.add_transactionServicer_to_server(Branch(id, balance, branches), server)
    server.add_insecure_port('[::]:'+str(50050+id))
    server.start()
    server.wait_for_termination()

def run_customer(id, events):
    """implement communication between customer and branch"""
    Customer(id, events).executeEvents()

def init_servers(branches, processids):
    """start multiple servers"""
    for branch in branches:
        worker = multiprocessing.Process(target=start_server, args=(branch['id'], branch['balance'], processids,))
        worker.start()

def run(customers):
    """implement mulitple customer and branch's communication"""
    for customer in customers:
        worker = multiprocessing.Process(target=run_customer,args=(customer['id'], customer['events'],))
        worker.start()

if __name__ == '__main__':
    # process input file
    branches, customers, processids = init_input()
    # start multiple servers
    init_servers(branches, processids)
    time.sleep(3)
    # implement multiple communications
    run(customers)
