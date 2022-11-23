from unittest import TestCase
import time
from stem.task_master import TaskMaster
from stem.task_runner import SimpleRunner, TaskRunner, ThreadingRunner, AsyncRunner, ProcessingRunner
from tests.example_tasks import int_scale


class RunnerTest(TestCase):

    def _run(self, runner: TaskRunner):
        task_master = TaskMaster(runner)
        result = task_master.execute({}, int_scale)
        for i, r in zip(range(0, 100, 10), result.data):
            self.assertEqual(i, r)

    def test_simple(self):
        start = time.time()
        runner = SimpleRunner()
        self._run(runner)
        end = time.time() - start
        print(end)

    def test_threading(self):
        start = time.time()
        runner = ThreadingRunner()
        self._run(runner)
        end = time.time() - start
        print(end)

    def test_async(self):
        start = time.time()
        runner = AsyncRunner()
        self._run(runner)
        end = time.time() - start
        print(end)

    def test_process(self):
        start = time.time()
        runner = ProcessingRunner()
        self._run(runner)
        end = time.time() - start
        print(end)
