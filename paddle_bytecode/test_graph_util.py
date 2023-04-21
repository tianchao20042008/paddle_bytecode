import unittest
import paddle_bytecode.graph_util as graph_util

class TestBfs(unittest.TestCase):
  def test_simple(self):
    next_nodes = {0:[1, 3], 1:[2], 2:[5], 3:[4], 4:[5]}
    def get_next_nodes(n): 
      if n in next_nodes:
        yield from next_nodes[n]
    bfs_visted = list(graph_util.bfs_visited_nodes([0], get_next_nodes))
    expected = [0, 1, 3, 2, 4, 5]
    self.assertEqual(bfs_visted, expected)

if __name__ == '__main__':
  unittest.main()
