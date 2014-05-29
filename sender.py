'''
    jsonrpc over email
    server side
    email sender
'''
class Sender:
    def __init__(self, ssl, user, password, host, fromaddr, \
                 port = None, toaddr = None):
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__from = fromaddr
        self.__to = toaddr
        self.__ssl = ssl
        self.__id = id(self)
        self.__client = None
        self.__send = False #connected
        
    def __del__(self):
        if(None != self.__client):
            self.__client.quit()
        self.__send = False

    def connect(self):
        import smtplib
        if(None != self.__port):
            if(self.__ssl):
                self.__port = 465
            else:
                self.__port = 25
                
        if(self.__ssl):
            self.__client = smtplib.SMTP_SSL(self.__host, self.__port)
        else:
            self.__client = smtplib.SMTP(self.__host, self.__port)
        self.__client.login(self.__user, self.__password)
        self.__send = True
            
    def getAddrs(self, fromaddr = None, toaddr = None):
        if(None == fromaddr):
            if(None != self.__from):
                fromaddr = self.__from
            else:
                print("error: no from address")
                return
        if(None == toaddr):
            if(None != self.__to):
                toaddr = self.__to
            else:
                print("error: no to address")
                return
        return fromaddr, toaddr

    def sendmail(self, text, fromaddr = None, toaddr = None):
        if(not self.__send):
            print('error: not loged in')
            return
        self.__client.sendmail(fromaddr, toaddr, text)

    def send(self, text, sub = None, fromaddr = None, toaddr = None):
        fromaddr, toaddr = self.getAddrs(fromaddr, toaddr)
        if(None != fromaddr):
            msg = self.getMsg(fromaddr, toaddr, text, sub)
            self.__client.sendmail(fromaddr, toaddr, msg)
        else:
            print('error: wrong address')
            
    def getMsg(self, fromaddr, toaddr, text, sub = None):
        from email.mime.text import MIMEText
        from email.header import Header
        msg = MIMEText(text, 'plain', 'utf8')
        msg['to'] = toaddr
        msg['from'] = fromaddr
        if(None == sub):
            sub = 'no subject'#163
        msg['subject'] = Header(sub, 'utf8')
        return msg.as_string()

    def getOnlineMsg(self, fromaddr, toaddr):
        if(not self.__send):
            print('error: not loged in')
            return
        return self.getMsg(fromaddr, toaddr, ('%d' % (self.__id)), 'id')
    
    def sendOnline(self, fromaddr = None, toaddr = None):
        if(not self.__send):
            print('error: not loged in')
            return
        import smtplib
        fromaddr, toaddr = self.getAddrs(fromaddr, toaddr)
        if(None != fromaddr):
            msg = self.getOnlineMsg(fromaddr, toaddr)
            self.__client.sendmail(fromaddr, toaddr, msg)
        else:
            print('error: wrong address')

    def getId(self):
        return self.__id

    def isConnected(self):
        return self.__send

if __name__=='__main__':
    client = Sender(False, 'pouloghost123', '', \
                    'smtp.163.com', 'pouloghost123@163.com',\
                    'pouloghost123@yeah.net')
    client.connect()
    client.send('{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}', '%d'%(client.getId()))
    
else:
    pass
