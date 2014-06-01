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

    def peekSubject(self, i):
        stat, byt = self.__client.fetch(i, 'BODY.PEEK[HEADER.FIELDS (SUBJECT)]') #to change
        return self.getString(byt, 'Subject')

    def pollMsgBody(self, i):
        stat, byt = self.__client.fetch(i, 'BODY[]')
        import email
        body = email.message_from_string(byt[0][1].decode(encoding = 'utf8')).\
                   get_payload(decode = True).decode()
        return body
    
    def pollWithFilter(self, mfilter):
        if(not self.__recv):
            print('error: not loged in')
            return 
        #criterion = '(SUBJECT "%d")' %(self.__id)
        criterion = '(NEW)'
        if(None == self.__box):
            self.__box = 'INBOX'
        self.__client.select(self.__box)
        stat, ids = self.__client.search(None, criterion)
        cids = []
        
        for i in ids[0].split():
            if(mfilter(i)):
                cids.append(i)
        return cids
    
    def pollRPCs(self):
        from email.header import Header
        msub = Header('%d' % (self.__id), 'utf8')
        msub = msub.encode()
        def mfilter(i):
            return self.peekSubject(i) == msub

        return self.pollWithFilter(mfilter)
    
    def updateId(self):
        from email.header import Header
        msub = Header('id', 'utf8')
        msub = msub.encode()
        def mfilter(i):
            return self.peekSubject(i) == msub
        ids = self.pollWithFilter(mfilter)
        result = None
        if(len(ids)!=0):
            i = ids[-1]
            mid = self.pollMsgBody(i)
            result = int(mid)
            self.__id = result
        return result
    
    def pollAll(self, cids):
        import email
        import rpc
        calls = []
        results = []
        for i in cids:
            json = rpc.parseJson(self.pollMsgBody(i))
            if('method' in json): #calls
                calls.append(json)
            else:
                print('result', json)
                results.append(json)
        return calls, results

    def isConnected(self):
        return self.__recv
        
if __name__ == '__main__':
    poller = Poller(False, 49856336, 'pouloghost123@yeah.net', '', 'imap.yeah.net',\
                    port = 143)
    poller.connect()
    print(poller.pollId())
