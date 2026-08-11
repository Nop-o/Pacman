from collections import deque


class DepthFirstSearch:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int]):
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit

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
            for neighbor in self.get_neighbors(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_cell
                    file.append(neighbor)
        return None

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        g = self.grid
        neighbors = []

        for direction in [g.NORTH, g.SOUTH, g.EAST, g.WEST]:
            if not (g.cells[y][x] & direction):
                dx, dy = g.DELTA[direction]
                nx, ny = x + dx, y + dy
                if g.is_valid(nx, ny):
                    neighbors.append((nx, ny))
        return neighbors

    def get_path_way(self,
                     parent: dict[tuple[int, int],
                                  tuple[int, int]
                                  | None]) -> list[tuple[int, int]]:
        path = []
        current = self.exit

        while current:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path


if __name__ == "__main__":
    pass
