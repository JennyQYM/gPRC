import grpc
import bank_pb2
import bank_pb2_grpc
import time
import datetime

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = self.createStub()

    def createStub(self):
        # connect the customer's corresponding bank's server
        channel = grpc.insecure_channel('localhost:{}'.format(str(50050 + self.id)))
        return bank_pb2_grpc.transactionStub(channel)

    def executeEvents(self):
        # prepare the output format
        res = {'id':self.id, 'recv':[]}

        # detect if any failure happend for each event
        successflag = 1
        for event in self.events:
            if event['interface'] != 'query':
                # send request to the bank and record it's request status
                try:
                    msg = self.stub.MsgDelivery(bank_pb2.transaction_request(type='customer', action=event['interface'], amount=event['money']))
                    self.recvMsg.append(msg)
                    res['recv'].append({'interface': event['interface'], 'result': 'success'})
                except:
                    res['recv'].append({'interface': event['interface'], 'result': 'fail'})
                    successflag = 0
                    break

        # sleep 3s to make sure all replica in each bank are the same
        time.sleep(3)
        if successflag:
            msg = self.stub.MsgDelivery(bank_pb2.transaction_request(type='customer', action='query'))
            self.recvMsg.append(msg)
            res['recv'].append({'interface': 'query', 'result': 'success', 'money': msg.balance})

        # generate output file
        f = open("output.txt", "a")
        f.write(str(res) +'\n')
        f.close()
