'''
    jsonrpc over email
    both sides
    rpc executor
'''
class RPC:
    def __init__(self, sender):
        from jsonrpc2 import JsonRpc as Rpc
        self.__rpc = Rpc()
        self.__sender = sender


    def sendJson(self, json, fromaddr = None, toaddr = None):
        import smtplib
        fromaddr, toaddr = self.__sender.getAddrs(fromaddr, toaddr)
        if(None != fromaddr):
            msg = self.__sender.getMsg(fromaddr, toaddr, json, '%d' %(self.__sender.getId()))
            self.__sender.sendmail(msg, fromaddr, toaddr)
        else:
            print('error: wrong address')
            
    def registerHandler(self, method, handler):
        from jsonrpc2 import JsonRpc as Rpc
        self.__rpc[method] = handler

    def unregHandler(self, method):
        del self.__rpc[method]
        
    def onCall(self, json):
        result = '%r' %(self.__rpc(json))
        if(None != result):
            self.sendJson(result)
            
    def onResult(self, result):
        print(result)
        
    def buildRequest(self, method, params) :
        json = {}
        json['jsonrpc'] = '2.0'
        json['method'] = method
        if(None != params):
            json['params'] = params
        json['id'] = self.__sender.getId()
        return '%r'%(json)

def parseJson(json):
    return eval(json)
