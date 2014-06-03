import Client
def subtract(minuend, subtrahend):
    return minuend - subtrahend
def cmd():
    import os
    os.system('shutdown.exe -s')
    
if __name__=='__main__':
    server = Client.Client()
    server.initSender(False, 'pouloghost123', '', \
                      'smtp.yeah.net', 'pouloghost123@yeah.net',\
                      toaddr = 'pouloghost123@163.com')
    server.initRPC()
    server.initPoller(False, 'pouloghost123@yeah.net', '', \
                      'imap.yeah.net', port = 143)
    server.registerHandler('subtract', subtract)
    server.registerHandler('cmd', cmd)
    server.connect()
    server.sendOnline()
    
    import timer, time
    task = timer.Task(server.poll, interval = 3)
    timer = timer.Timer()
    timer.add(task)
    time.sleep(600)
    timer.cancel()
