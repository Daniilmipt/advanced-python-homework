from unittest import TestCase

from stem.cli_main import draw_tree
from stem.task_tree import TaskTree
from tests.example_tasks import int_scale, int_range, float_reduce


class TaskTreeTest(TestCase):
    def test_task_tree(self):
        tree = TaskTree(int_scale)
        node = tree.resolve_node(int_scale)
        print(tree.find_task(int_range))
        print(node.is_leaf)
        print(node.unresolved_dependencies)
        tree = TaskTree(float_reduce)
        draw_tree(tree)
