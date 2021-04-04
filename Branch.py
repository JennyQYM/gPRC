import grpc
import bank_pb2
import bank_pb2_grpc
import os

class Branch(bank_pb2_grpc.transactionServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = [self.GenerateStubList(id) for id in self.branches]
        # a list of received messages used for debugging purpose
        self.recvMsg = list()

    def MsgDelivery(self, request, context):
        self.recvMsg.append(request)
        if request.action == 'query':
            return bank_pb2.transaction_reply(balance=self.Query())

        if request.action == 'withdraw':
            if request.type == 'customer':
                self.Propogate_Withdraw(request.amount)
            if request.type == 'branch':
                self.Withdraw(request.amount)
            return bank_pb2.transaction_reply(balance=self.Query())

        if request.action == 'deposit':
            if request.type == 'customer':
                self.Propogate_Deposit(request.amount)
            if request.type == 'branch':
                self.Depostit(request.amount)
            return bank_pb2.transaction_reply(balance=self.Query())


    def Query(self):
        return self.balance

    def Withdraw(self, amount):
        self.balance -= amount

    def Depostit(self, amount):
        self.balance += amount

    def Propogate_Withdraw(self, amount):
        for stub in self.stubList:
            stub.MsgDelivery(bank_pb2.transaction_request(type='branch', action='withdraw', amount=amount))

    def Propogate_Deposit(self, amount):
        for stub in self.stubList:
            stub.MsgDelivery(bank_pb2.transaction_request(type='branch', action='deposit', amount=amount))

    def GenerateStubList(self, id):
        channel = grpc.insecure_channel('localhost:{}'.format(str(50050+id)))
        return bank_pb2_grpc.transactionStub(channel)
