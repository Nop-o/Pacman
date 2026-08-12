from collections import deque
from ..maze import Maze


class DepthFirstSearch:
    def __init__(self, entry: tuple[int, int],
                 exit: tuple[int, int], maze: Maze):
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.maze: Maze = maze

    def solver(self) -> list[tuple[int, int]] | None:
        parent: dict[tuple[int, int],
                     tuple[int, int] | None] = {self.entry: None}
        visited: set[tuple[int, int]] = {self.entry}
        file: deque[tuple[int, int]] = deque([self.entry])

        while file:
            current_cell: tuple[int, int] = file.popleft()
            if current_cell == self.exit:
                return self.get_path_way(parent)
            x, y = current_cell
            for neighbor in self.get_neighbors_coord(y, x):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_cell
                    file.append(neighbor)
        return None

    def get_neighbors_coord(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = self.maze.get_neighbors(self.maze.get_case(y, x))
        neighbors_coord = []
        for neighbor in neighbors:
            neighbors_coord.append(neighbor.get_coordinate())
        return neighbors_coord

    def get_path_way(self,
                     parent: dict[tuple[int, int],
                                  tuple[int, int]
                                  | None]) -> list[tuple[int, int]]:
        path = []
        current: tuple[int, int] | None = self.exit

        while current:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path


if __name__ == "__main__":
    maze = Maze(5)
    dfs = DepthFirstSearch((1, 1), (1, 2), maze)
    result = dfs.solver()
    print(result)
