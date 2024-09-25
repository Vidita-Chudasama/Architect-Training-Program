import threading
import time
import queue
import random
from datetime import datetime, timedelta

class Producer(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        task_id = 1
        while True:
            # Produce a new task and a random time interval (in seconds) for execution
            task = f"Task-{task_id}"
            delay = random.randint(1, 5)

            # Calculate the task's scheduled execution time
            execution_time = datetime.now() + timedelta(seconds=delay)

            print(f"Producer: Generated {task} scheduled to run in {delay} seconds (at {execution_time})")

            # Put the task in the queue with its execution time (use a tuple with priority based on execution time)
            self.task_queue.put((execution_time, task))

            task_id += 1
            time.sleep(random.randint(2, 4))  # Wait before generating the next task


class Consumer(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        while True:
            # Get the next task from the queue
            execution_time, task = self.task_queue.get()

            # Calculate how long to wait until the task is due to execute
            now = datetime.now()
            wait_time = (execution_time - now).total_seconds()

            if wait_time > 0:
                print(f"Consumer: Waiting {wait_time:.2f} seconds to execute {task}")
                time.sleep(wait_time)

            # Execute the task after waiting the required amount of time
            print(f"Consumer: Executing {task} at {datetime.now()}")

            # Mark the task as done
            self.task_queue.task_done()


if __name__ == "__main__":
    # Priority queue to store tasks based on their execution time
    task_queue = queue.PriorityQueue()

    producer = Producer(task_queue)
    producer.start()

    consumer = Consumer(task_queue)
    consumer.start()

    producer.join()
    consumer.join()
