import queue
import threading
import time

class Connection:
    def __init__(self, id):
        self.id = id

    def connect(self):
        time.sleep(0.1)  # Simulate connection delay
        print(f"Connection {self.id} established.")

    def close(self):
        print(f"Connection {self.id} closed.")

class SimpleConnectionPool:
    def __init__(self, max_size=5):
        self.max_size = max_size
        self.pool = queue.Queue(maxsize=max_size)
        self.lock = threading.Lock()

        for i in range(max_size):
            connection = Connection(i + 1)
            self.pool.put(connection)

    def acquire(self):
        connection = self.pool.get()
        print(f"Acquired connection {connection.id}")
        return connection

    def release(self, connection):
        print(f"Releasing connection {connection.id}")
        self.pool.put(connection)

    def close_all(self):
        with self.lock:
            while not self.pool.empty():
                connection = self.pool.get()
                connection.close()


def use_connection(pool):
    connection = pool.acquire()
    connection.connect()
    time.sleep(0.5)  # do something
    pool.release(connection)

if __name__ == "__main__":
    pool = SimpleConnectionPool(max_size=3)

    threads = []
    for _ in range(6):
        t = threading.Thread(target=use_connection, args=(pool,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    pool.close_all()
