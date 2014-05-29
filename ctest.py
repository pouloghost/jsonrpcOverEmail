import Client
if __name__=='__main__':
    client = Client.Client()
    client.initSender(False, 'pouloghost123', '942646', \
                    'smtp.163.com', 'pouloghost123@163.com',\
                    toaddr = 'pouloghost123@yeah.net')
    client.initRPC()
    client.initPoller(False, 'pouloghost123@163.com', '942646', \
                      'imap.163.com', port = 143)
    client.connect()
    client.sendOnline()
    client.sendRequest('subtract', [42, 43])
    
