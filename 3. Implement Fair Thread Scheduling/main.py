import threading
import collections
import time

class LegalReentrantLock:
    def __init__(self):
        self._lock = threading.Lock()
        self._owner = None
        self._recursion_count = 0
        self._wait_queue = collections.deque()
        self._condition = threading.Condition(self._lock)  # For signaling waiting threads

    def acquire(self):
        current_thread = threading.current_thread()

        with self._condition:
            # Check if current thread already owns the lock (reentrant behavior)
            if self._owner == current_thread:
                self._recursion_count += 1
                return
            
            # If another thread owns the lock, add the current thread to the wait queue
            self._wait_queue.append(current_thread)
            
            # Wait until it's the current thread's turn (FIFO)
            while self._owner is not None or self._wait_queue[0] != current_thread:
                self._condition.wait()

            self._wait_queue.popleft()  # Remove thread from queue
            self._owner = current_thread
            self._recursion_count = 1

    def release(self):
        current_thread = threading.current_thread()

        with self._condition:
            if self._owner != current_thread:
                raise RuntimeError("Cannot release a lock owned by another thread")

            self._recursion_count -= 1

            # If recursion count reaches 0, release the lock completely
            if self._recursion_count == 0:
                self._owner = None
                self._condition.notify_all()  # Notify other waiting threads

    def is_locked(self):
        with self._condition:
            return self._owner is not None


def worker(lock, thread_id):
    print(f"Thread {thread_id} is trying to acquire the lock...")
    lock.acquire()
    print(f"Thread {thread_id} has acquired the lock.")

    print(f"Thread {thread_id} is re-acquiring the lock (reentrancy)...")
    lock.acquire()
    print(f"Thread {thread_id} has re-acquired the lock.")

    # Do some work
    time.sleep(1)

    print(f"Thread {thread_id} is releasing the lock once...")
    lock.release()

    print(f"Thread {thread_id} is releasing the lock completely...")
    lock.release()
    print(f"Thread {thread_id} has released the lock fully.\n")


if __name__ == "__main__":
    lock = LegalReentrantLock()

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(lock, i+1))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("All threads have finished execution.")
