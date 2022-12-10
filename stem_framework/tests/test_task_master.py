import json
from unittest import TestCase

from stem.task_master import TaskMaster
from stem.task_runner import SimpleRunner
from tests.example_tasks import int_scale
from tests.example_workspace import IntWorkspace


class SimpleRunnerTest(TestCase):

    def setUp(self) -> None:
        self.runner = SimpleRunner()

    def test_execute(self):
        task_master = TaskMaster(self.runner)
        result = task_master.execute({}, int_scale)
        print(list(zip([], result.data)))
        # print(IntWorkspace.tasks)
        # result = task_master.execute({}, IntWorkspace.int_scale)
        # print(result.data)
        print(json.dumps({'task_result': "fdd"}))
        # for i, r in zip(range(0, 100, 10), result.lazy_data()):
        #     self.assertEqual(i, r)
