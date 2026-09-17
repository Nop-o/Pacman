from collections import deque
from ..maze import Maze


class DepthFirstSearch:
    """Pathfind between two maze cells using breadth-first search."""

    def __init__(self, maze: Maze):
        """Initialize the solver with an empty entry and exit.

        Args:
            maze: The maze to search within.
        """
        self._entry: tuple[int, int] | None = None
        self._exit: tuple[int, int] | None = None
        self.maze: Maze = maze

    def solver(self) -> list[tuple[int, int]] | None:
        """Find the shortest path from the entry to the exit.

        Returns:
            The list of (line, column) positions forming the path, or None
            if no path exists.

        Raises:
            ValueError: If entry or exit have not been set.
        """
        entry_ = self.entry
        exit_ = self.exit
        if entry_ is None or exit_ is None:
            raise ValueError("Entry and exit must be set before solving")

        parent: dict[tuple[int, int],
                     tuple[int, int] | None] = {entry_: None}
        visited: set[tuple[int, int]] = {entry_}
        file: deque[tuple[int, int]] = deque([entry_])

        while file:
            current_cell: tuple[int, int] = file.popleft()
            if current_cell == exit_:
                return self.get_path_way(parent)
            x, y = current_cell
            for neighbor in self.get_neighbors_coord(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_cell
                    file.append(neighbor)
        return None

    def get_neighbors_coord(self, x: int, y: int) -> list[tuple[int, int]]:
        """Get the coordinates of all accessible neighboring cells.

        Args:
            x: Line position of the cell.
            y: Column position of the cell.

        Returns:
            A list of (line, column) coordinates of neighboring cells.
        """
        neighbors = self.maze.get_neighbors(self.maze.get_case((x, y)))
        neighbors_coord = []
        for neighbor in neighbors:
            neighbors_coord.append(neighbor.get_coordinate())
        return neighbors_coord

    def get_path_way(self,
                     parent: dict[tuple[int, int],
                                  tuple[int, int]
                                  | None]) -> list[tuple[int, int]]:
        """Reconstruct the path from entry to exit using parent links.

        Args:
            parent: Mapping of each visited cell to the cell it was reached
                from.

        Returns:
            The list of (line, column) positions forming the path, from
            entry to exit.
        """
        path = []
        current: tuple[int, int] | None = self.exit

        while current:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    @property
    def exit(self) -> tuple[int, int] | None:
        """Return the current exit position.

        Returns:
            The (line, column) exit position.

        Raises:
            ValueError: If the exit has not been set.
        """
        if self._exit is None:
            raise ValueError(
                f"{type(self).__name__} hasn't initialized self._exit")

        return self._exit

    @property
    def entry(self) -> tuple[int, int] | None:
        """Return the current entry position.

        Returns:
            The (line, column) entry position.

        Raises:
            ValueError: If the entry has not been set.
        """
        if self._entry is None:
            raise ValueError(
                f"{type(self).__name__} hasn't initialized self._entry")

        return self._entry

    def set_exit(self, exit: tuple[int, int] | None) -> None:
        """Set the exit position.

        Args:
            exit: The new (line, column) exit position.
        """
        self._exit = exit

    def set_entry(self, entry: tuple[int, int] | None) -> None:
        """Set the entry position.

        Args:
            entry: The new (line, column) entry position.
        """
        self._entry = entry
