import multiprocessing
import queue
import time

class BaseSpiderProcess:
    def __init__(self, worker_num: int = 4):
        self.task_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        self.workers = []
        self.worker_num = worker_num
        
    def add_task(self, task):
        self.task_queue.put(task)
        
    def worker_process(self):
        while True:
            try:
                task = self.task_queue.get(timeout=30)
                result = self.process_task(task)
                self.result_queue.put(result)
            except queue.Empty:
                break
                
    def process_task(self, task):
        raise NotImplementedError("Subclasses must implement process_task")
        
    def start(self):
        for _ in range(self.worker_num):
            p = multiprocessing.Process(target=self.worker_process)
            p.start()
            self.workers.append(p)
            
    def get_results(self):
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results
    
    def wait_completion(self):
        for p in self.workers:
            p.join()
