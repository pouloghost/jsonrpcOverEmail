'''
    jsonrpc over email
    client side
    email sender
'''
class Poller:
    def __init__(self, ssl, jid, user, password, host, \
                 port = None, mailbox = None):
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__ssl = ssl
        self.__id = jid
        self.__box = mailbox
        self.__client = None
        self.__recv = False #connected

    def __del__(self):
        if(None != self.__client):
            self.__client.quit()
        self.__recv = False

    def connect(self):
        import imaplib
        if(None == self.__port):
            if(self.__ssl):
                self.__port = 993
            else:
                self.__port = 143

        if(self.__ssl):
            self.__client = imaplib.IMAP4_SSL(self.__host, self.__port)
        else:
            self.__client = imaplib.IMAP4(self.__host, self.__port)
        self.__client.login(self.__user, self.__password)
        self.__recv = True

    def getString(self, byt, key):
        import email
        return email.message_from_string(byt[0][1].decode(encoding = 'utf8'))[key]
    
    def pollRPCs(self):
        if(not self.__recv):
            print('error: not loged in')
            return 
        from email.header import Header
        #criterion = '(SUBJECT "%d")' %(self.__id)
        criterion = '(NEW)'
        if(None == self.__box):
            self.__box = 'INBOX'
        self.__client.select(self.__box)
        stat, ids = self.__client.search(None, criterion)
        cids = []
        #a header string
        mfilter = Header('%d' % (self.__id), 'utf8')
        mfilter = mfilter.encode()
        
        for i in ids[0].split():
            stat, byt = self.__client.fetch(i, 'BODY[HEADER.FIELDS (SUBJECT)]') #to change
            sub = self.getString(byt, 'Subject')
            if(sub == mfilter):
                cids.append(i)
        return cids
    
    def pollAll(self, cids):
        import email
        import rpc
        calls = []
        results = []
        for i in cids:
            stat, byt = self.__client.fetch(i, 'BODY[]')
            json = rpc.parseJson(email.message_from_string(byt[0][1].decode(encoding = 'utf8')).\
                   get_payload(decode = True).decode())
            if('method' in json): #calls
                calls.append(json)
            else:
                results.append(json)
        return calls, results

    def isConnected(self):
        return self.__recv

if __name__ == '__main__':
    poller = Poller(False, 49856336, 'pouloghost123@yeah.net', '', 'imap.yeah.net',\
                    port = 143)
    poller.connect()
    calls = poller.pollCallIds();
    print(poller.pollCalls(calls))
