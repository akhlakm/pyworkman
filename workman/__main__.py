from workman import broker, backend
from multiprocessing import Process

def main():
    p1 = Process(target=broker.start)
    p2 = Process(target=backend.start)

    p1.start()
    p2.start()
    p1.join()
    p2.join()
