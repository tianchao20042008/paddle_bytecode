from typing import List, Callable, Any, Iterator, Dict, Set

# Generate bfs visted nodes
def bfs_visited_nodes(starts: List[Any],
                      get_next_nodes: Callable[[Any], Iterator[Any]]):
  visited: Set[Any] = set()
  queue: List[Any] = starts[:]
  while len(queue) > 0:
    current = queue[0]
    del queue[0]
    if current in visited:
      continue
    yield current
    visited.add(current)
    for next_node in get_next_nodes(current):
      queue.append(next_node)
