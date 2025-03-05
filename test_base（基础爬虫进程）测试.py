import pytest
import queue
from base_spidernet.base_resolver import BaseSpiderProcess, BaseResolver

class TestSpiderProcess(BaseSpiderProcess):
    def process_task(self, task):
        return task * 2

class TestBaseSpider:
    def test_full_workflow(self):
        spider = TestSpiderProcess(worker_num=2)
        spider.add_task(1)
        spider.add_task(2)
        spider.start()
        spider.wait_completion()
        results = spider.get_results()
        assert sorted(results) == [2, 4]
        
    def test_queue_timeout(self, mocker):
        mocker.patch('queue.Queue.get', side_effect=queue.Empty)
        spider = TestSpiderProcess()
        spider.start()
        spider.wait_completion()
        assert len(spider.get_results()) == 0

    def test_process_task_not_implemented(self):
        base = BaseSpiderProcess()
        with pytest.raises(NotImplementedError):
            base.process_task(None)
