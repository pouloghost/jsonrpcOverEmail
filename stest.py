import Client
def subtract(minuend, subtrahend):
    return minuend - subtrahend

if __name__=='__main__':
    server = Client.Client()
    server.initSender(False, 'pouloghost123', '', \
                      'smtp.yeah.net', 'pouloghost123@yeah.net',\
                      toaddr = 'pouloghost123@163.com')
    server.initRPC()
    server.initPoller(False, 'pouloghost123@yeah.net', '', \
                      'imap.yeah.net', port = 143, jid = 0000)
    server.registerHandler('subtract', subtract)
    server.connect()
    server.updateId()
    import timer, time
    task = timer.Task(server.poll, interval = 30)
    timer = timer.Timer()
    timer.add(task)
    time.sleep(600)
    timer.cancel()
