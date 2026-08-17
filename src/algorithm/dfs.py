from collections import deque
from ..maze import Maze


class DepthFirstSearch:
    def __init__(self, maze: Maze):
        self._entry: tuple[int, int] | None = None
        self._exit: tuple[int, int] | None = None
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

    @property
    def exit(self) -> tuple[int, int] | None:
        if self._exit is None:
            raise ValueError(
                f"{type(self).__name__} hasn't initialized self._exit")

        return self._exit

    @property
    def entry(self) -> tuple[int, int] | None:
        if self._entry is None:
            raise ValueError(
                f"{type(self).__name__} hasn't initialized self._entry")

        return self._entry

    def set_exit(self, exit: tuple[int, int] | None) -> None:
        self._exit = exit

    def set_entry(self, entry: tuple[int, int] | None) -> None:
        self._entry = entry


if __name__ == "__main__":
    maze = Maze(5)
    dfs = DepthFirstSearch(maze)
    dfs.set_exit((1,1))
    dfs.set_entry((2, 2))
    result = dfs.solver()
    print(result)
