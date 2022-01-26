import threading
def printit():
    print('start')
    threading.Timer(5.0, printit).start() 

var = "start" 
printit()