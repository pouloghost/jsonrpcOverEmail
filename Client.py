import sender
import poller
import rpc
'''
    jsonrpc over email
    overall wrapper
'''
class Client:
    def __init__(self):
        self.__ok = False
        
    def initSender(self, ssl, user, password, host, fromaddr, \
                 port = None, toaddr = None):
        self.__sender = sender.Sender(ssl, user, password, host, fromaddr,\
                                      port, toaddr)
        print('sender init')
        
    def initRPC(self):
        self.__rpc = rpc.RPC(self.__sender)
        print('rpc init')

    def initPoller(self, ssl, user, password, host, \
                 jid = None ,port = None, mailbox = None):
        if(None == jid):
            jid = self.__sender.getId()
        self.__poller = poller.Poller(ssl, jid, user, password, host, \
                 port, mailbox)
        print('poller init')

    def connect(self):
        print('connecting...')
        self.__sender.connect()
        self.__poller.connect()
        self.__ok = self.__sender.isConnected() and self.__poller.isConnected()
        if(not self.__ok):
            print('error: not connected')
            exit(1)
        print('connected')

    def sendOnline(self):
        self.__sender.sendOnline()
        print('online')

    def sendRequest(self, method, params):
        json = self.__rpc.buildRequest(method, params)
        self.__rpc.sendJson(json)
        print('request %r'%(json))

    def registerHandler(self, method, handler):
        self.__rpc.registerHandler(method, handler)

    def unregHandler(self, method):
        self.__rpc.unregHandler(method)

    def poll(self):
        cids = self.__poller.pollRPCs()
        print(cids)
        calls, results = self.__poller.pollAll(cids)
        for call in calls:
            print('call %r'%(call))
            self.__rpc.onCall(call)
        for result in results:
            print('result %r'%(result))
            self.__rpc.onResult(result)


if __name__=='__main__':
    client = Client()
    client.initSender(False, 'pouloghost123', '942646', \
                    'smtp.163.com', 'pouloghost123@163.com',\
                    'pouloghost123@yeah.net')
    client.initRPC()
    client.initPoller(False, 'pouloghost123@yeah.net', '942646', \
                      'imap.yeah.net', port = 143)
    client.connect()
    client.sendOnline()
    client.sendRequest('subtract', [42, 43])

    server = Client()
    server.initSender(False, 'pouloghost123', '942646', \
                      'smtp.yeah.net', 'pouloghost123@yeah.net',\
                      'pouloghost123@163.com')
    server.initRPC()
    server.initPoller(False, 'pouloghost123@163.com', '942646', \
                      'imap.163.com', port = 143)
    server.registerHandler('subtract', subtract)
    server.poll()
    
else:
    pass
