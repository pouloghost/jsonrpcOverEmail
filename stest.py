import Client
def subtract(minuend, subtrahend):
    return minuend - subtrahend

if __name__=='__main__':
    server = Client.Client()
    server.initSender(False, 'pouloghost123', '942646', \
                      'smtp.yeah.net', 'pouloghost123@yeah.net',\
                      toaddr = 'pouloghost123@163.com')
    server.initRPC()
    server.initPoller(False, 'pouloghost123@yeah.net', '942646', \
                      'imap.yeah.net', port = 143, jid = 50330000)
    server.registerHandler('subtract', subtract)
    server.connect()
    server.poll()
