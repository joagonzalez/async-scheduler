from tasks import add, wait_seconds
import time

_ok = False

while True:
    result = add.delay(4, 4)
    result2 = add.delay(2,9)

    # this is not the idea because we are generating synchronous communication
    # but helps to the example
    while not (result.ready() and result2.ready()):
        if not _ok:
            print('result 1: ' + str(result.ready()))
            print('result 2: ' + str(result2.ready()))
        
        _ok = True
    _ok = False

    print('result 1: ' + str(result.ready()))
    print('result 2: ' + str(result2.ready()))    
    
    get = result.get(propagate=False)
    get2 = result2.get(propagate=False)
    
    print('Result of task ' + str(result) + '  is ' + str(get))
    print('Result of task ' + str(result2) + '  is ' + str(get2))  
    time.sleep(1)