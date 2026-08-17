#  src

# - cheat
# - game_state

#---------------------------
##  algorithm

##  - dfs
# if __name__ == "__main__":
#     maze = Maze(5)
#     dfs = DepthFirstSearch(maze)
#     dfs.set_exit((1,1))
#     dfs.set_entry((2, 2))
#     result = dfs.solver()
#     print(result)

#---------------------------

##  entity

##  - character
# if __name__ == "__main__":
#     maze = Maze()
#     chara = Character(maze, 10)

##  - entity

##  - ghost
# if __name__ == "__main__":
#     maze = Maze()
#     algo = DepthFirstSearch(maze)
#     algo.set_exit((1,1))
#     algo.set_entry((2, 2))
#     pacman = Pacman(3, maze, 10)
#     ghost1 = Pokey(maze, pacman, 10, algo)
#     ghost2 = Shadow(maze, pacman, 10, algo)
#     ghost3 = Speedy(maze, pacman, 10, algo)
#     ghost4 = Bashful(maze, pacman, 10, algo)


##  - pacgum

##  - pacman
# if __name__ == "__main__":
#     maze = Maze()
#     pacman = Pacman(lives=3, maze=maze, super_pacgum_cooldown=90) 

#---------------------------

##  maze

##  - case
##  - maze

#---------------------------

##  parsing

##  - json_parsing
# if __name__ == "__main__":
#     parser = JsonParsing("settings.json", "setting.json")
#     print(parser.file_content)

#---------------------------

## visual_simulation

##  - screen_manager
# if __name__ == "__main__":
#     from .. import GameState
#     from ..entity import Pacman, Bashful, Shadow, Speedy, Pokey
#     from ..maze import Maze
#     from ..algorithm import DepthFirstSearch

#     maze = Maze()
#     algo = DepthFirstSearch(maze=maze)
#     pacman = Pacman(lives=10, maze=maze, super_pacgum_cooldown=10)

#     ghost_1 = Bashful(
#         maze=maze,pacman=pacman, super_pacgum_cooldown=10, algorithm=algo)
#     ghost_2 = Shadow(
#         maze=maze, pacman=pacman, super_pacgum_cooldown=10, algorithm=algo)
#     ghost_3 = Speedy(
#         maze=maze, pacman=pacman, super_pacgum_cooldown=10, algorithm=algo)
#     ghost_4 = Pokey(
#         maze=maze, pacman=pacman, super_pacgum_cooldown=10, algorithm=algo)

#     game_state = GameState(pacgum=10, points_per_pacgum=100,
#                            points_per_super_pacgum=10, super_pacgum_time=10,
#                            points_per_ghost=1000, seed=42, level_max_time=200,
#                            pacman=pacman, ghosts=[ghost_1, ghost_2, ghost_3, ghost_4])
#     level = Level(game_state)

#     sceen_manager = ScreenManager(game_state=game_state, level=level)

##  - simulation_manager

#---------------------------

###screen

###  - game_over
# if __name__ == "__main__":
#     leaderboard = LeaderBoard()
#     game_over = GameOver(leaderboard)

###  - game_play
# if __name__ == "__main__":
#     from ... import GameState
#     from ...entity import Pacman
#     from ...entity import Ghost, Bashful, Shadow, Speedy, Pokey
#     from ...maze import Maze
#     from ...algorithm import DepthFirstSearch
#     from . import Level

#     maze = Maze()
#     algo = DepthFirstSearch(maze=maze)
#     pacman = Pacman(lives=10, maze=maze, super_pacgum_cooldown=10)

#     ghost_1 = Bashful(maze=maze, starting_position=(10, 10), pacman=pacman,
#                     super_pacgum_cooldown=10, algorithm=algo)
#     ghost_2 = Shadow(maze=maze, starting_position=(11, 11), pacman=pacman,
#                     super_pacgum_cooldown=10, algorithm=algo)
#     ghost_3 = Speedy(maze=maze, starting_position=(12, 12), pacman=pacman,
#                     super_pacgum_cooldown=10, algorithm=algo)
#     ghost_4 = Pokey(maze=maze, starting_position=(13, 13), pacman=pacman,
#                     super_pacgum_cooldown=10, algorithm=algo)

#     game_state = GameState(pacgum=10, points_per_pacgum=100,
#                            points_per_super_pacgum=10, super_pacgum_time=10,
#                            points_per_ghost=1000, seed=42, level_max_time=200,
#                            pacman=pacman,
#                            ghosts=[ghost_1, ghost_2, ghost_2, ghost_4])

#     hud = HUD(game_state)
#     level = Level(game_state)
#     gameplay = GamePlay(level, hud)

###  - hud
# if __name__ == "__main__":
#     from ... import GameState
#     from ...entity import Pacman
#     from ...entity import Ghost, Bashful, Shadow, Speedy, Pokey
#     from ...maze import Maze
#     from ...algorithm import DepthFirstSearch
#     from . import Level
#     maze = Maze()
#     algo = DepthFirstSearch(maze=maze)
#     pacman = Pacman(lives=10, maze=maze, super_pacgum_cooldown=10)
#     ghost_1 = Bashful(maze=maze, starting_position=(10, 10), pacman=pacman,
#                     super_pacgum_cooldown=10, algorithm=algo)
#     ghost_2 = Shadow(maze=maze, starting_position=(11, 11), pacman=pacman,
#                     super_pacgum_cooldown=10, algorithm=algo)
#     ghost_3 = Speedy(maze=maze, starting_position=(12, 12), pacman=pacman,
#                     super_pacgum_cooldown=10, algorithm=algo)
#     ghost_4 = Pokey(maze=maze, starting_position=(13, 13), pacman=pacman,
#                     super_pacgum_cooldown=10, algorithm=algo)
#     game_state = GameState(pacgum=10, points_per_pacgum=100,
#                            points_per_super_pacgum=10, super_pacgum_time=10,
#                            points_per_ghost=1000, seed=42, level_max_time=200,
#                            pacman=pacman,
#                            ghosts=[ghost_1, ghost_2, ghost_2, ghost_4])
#     hud = HUD(game_state=game_state)

###  - leaderboard
# if __name__ == "__main__":
#     leaderboard = LeaderBoard()
#     print(f"{leaderboard.scores}: {leaderboard.names}")
#     leaderboard.update_leaderboard(1, 3000, "yohan")
#     leaderboard.add_new_highscore(10000, "nico")
#     print(f"{leaderboard.scores}: {leaderboard.names}")

###  - level
###  - main_menu
###  - pause_menu
###  - screen
###  - victory