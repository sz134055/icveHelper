import time
from concurrent.futures import ThreadPoolExecutor


def testIt():
    time.sleep(10)
    print('TEST')



if __name__ == '__main__':
    thread = ThreadPoolExecutor(max_workers=2)
    thread.submit(testIt)
    thread.shutdown(wait=False)
    print('KILL ALL')
    thread.submit(testIt)
    print('AGAIN')
