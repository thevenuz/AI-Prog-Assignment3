from copy import deepcopy


class Maze:

    def __init__(self, maze) -> None:
        self.player = "R"
        self.opponent = "G"
        self.maze = maze
        self.depth = 3
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.player_position = (1, 1)
        self.opponent_position = (9, 19)
        self.tried_moves = []

    def minimax(self, maze, depth, maximizing_player):
        """Minimax algorithm implementation for the given maze."""

        if depth == 0 or self.is_game_finished():
            return self.evaluate(maze, maximizing_player), None

        if maximizing_player:
            max_eval = float("-inf")
            best_move = None

            # Get all possible moves for the player red.
            for move in self.get_all_moves(maze, maximizing_player):
                # Create a temporary maze to simulate the move.
                temp_maze = deepcopy(maze)
                new_maze = self.simulate_move(temp_maze, move, maximizing_player)

                # Recursively call the minimax function with the new maze that has the simulated move applied.
                evaluate_move = self.minimax(new_maze, depth - 1, False)[0]

                if evaluate_move >= max_eval:
                    max_eval = evaluate_move
                    best_move = move

            return max_eval, best_move

        else:
            min_eval = float("inf")
            best_move = None

            # Get all possible moves for the player green.
            for move in self.get_all_moves(maze, maximizing_player):

                # Create a temporary maze to simulate the move.
                temp_maze = deepcopy(maze)
                new_maze = self.simulate_move(temp_maze, move, maximizing_player)

                # Recursively call the minimax function with the new maze that has the simulated move applied.
                evaluate_move = self.minimax(new_maze, depth - 1, True)[0]

                if evaluate_move <= min_eval:
                    min_eval = evaluate_move
                    best_move = move

            return min_eval, best_move

    def is_game_finished(self):
        """Checks if the game is finished."""

        is_red_present = False
        is_green_present = False
        for r in self.maze:
            if "R" in r:
                is_red_present = True
            if "G" in r:
                is_green_present = True

        # Meaning red has won the game, since green is not present or red reached the other end
        if not is_green_present or self.maze[9][19] == "R":
            return True

        # Meaning green has won the game, since red is not present or green reached the other end
        elif not is_red_present or self.maze[1][1] == "G":
            return True

        return False

    def simulate_move(self, maze, move, maximizing_player):
        """Simulates the move on the temporary maze."""

        player_ = "R" if maximizing_player else "G"
        new_r, new_c = move

        for r in range(self.rows):
            for c in range(self.cols):
                if maze[r][c] == player_:
                    maze[r][c] = "."

        maze[new_r][new_c] = player_

        return maze

    def get_all_moves(self, maze, maximizing_player):
        """Get all possible moves for the player based on the current position."""

        player_ = "R" if maximizing_player else "G"
        possible_moves = []
        for r in range(1, self.rows, 2):
            for c in range(1, self.cols, 2):
                if maze[r][c] == player_:
                    # Check upward direction
                    if (r > 0 and maze[r - 1][c] != "X" and (maze[r - 2][c] == "." or maze[r - 2][c] == "G" or maze[r - 2][c] == "R")):
                        possible_moves.append((r - 2, c))

                    # Check downward direction
                    if (r < self.rows - 1 and maze[r + 1][c] != "X" and (maze[r + 2][c] == "." or maze[r + 2][c] == "G" or maze[r + 2][c] == "R")):
                        possible_moves.append((r + 2, c))

                    # Check left direction
                    if (c > 0 and maze[r][c - 1] != "X" and (maze[r][c - 2] == "." or maze[r][c - 2] == "G" or maze[r][c - 2] == "R")):
                        possible_moves.append((r, c - 2))

                    # Check right direction
                    if (c < self.cols - 1 and maze[r][c + 1] != "X" and (maze[r][c + 2] == "." or maze[r][c + 2] == "G" or maze[r][c + 2] == "R")):
                        possible_moves.append((r, c + 2))

        return possible_moves

    def check_if_starting_position(self, maze):
        """Check if the player is at the starting position."""

        if maze[1][1] == "R":
            return True
        if maze[9][19] == "G":
            return True
        return False

    def evaluate(self, maze, player):
        """This function evaluates the current maze and returns a score based on different criteria."""

        player_pos, opponent_pos = self.player_position, self.opponent_position

        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                if cell == "R":
                    player_pos = (i, j)
                if cell == "G":
                    opponent_pos = (i, j)

        # Provide a reward if the player is close to the goal.
        close_to_goal_reward = player_pos[0] - 9 + player_pos[1] - 19

        # Penalize the player if they are trying the previously used move.
        tried_move_penalty = (
            100 if player_pos or opponent_pos in self.tried_moves else 0
        )

        # Check if the player is at the starting position
        is_starting_position = self.check_if_starting_position(maze)

        starting_position_penalty = 100 if is_starting_position else 0

        # Calculate distances between player and opponent
        player_distance = abs(player_pos[0] - opponent_pos[0]) + abs(
            player_pos[1] - opponent_pos[1]
        )

        # Check if the player is close to a wall
        player_near_wall = self.check_if_neighbor_is_wall(maze, player_pos)

        # Penalize the player if they are near a wall
        wall_penalty = 10 if player_near_wall else 0

        # Determine the score based on penalties and rewards and player distance.
        if player == "R":
            evaluation = 100+ player_distance * 100 - wall_penalty - starting_position_penalty - tried_move_penalty + close_to_goal_reward * 10
            
        else:
            evaluation = -100 - player_distance * 100 - wall_penalty - starting_position_penalty - tried_move_penalty

        return evaluation

    def check_if_neighbor_is_wall(self, maze, pos):
        """Check if the neighbor cells of the current position are walls."""

        if (pos[0] - 1 > 0 and (maze[pos[0] - 1][pos[1]] or maze[pos[0] - 3][pos[1]]) == "X"):
            return True
        
        if (pos[0] < self.rows - 1 and ( maze[pos[0] + 1][pos[1]] or maze[pos[0] + 3][pos[1]] or maze[pos[0] + 5][pos[1]]) == "X"):
            return True
        
        if pos[1] - 1 > 0 and (maze[pos[0]][pos[1] - 1]) == "X":
            return True
        
        if (pos[1] < self.cols - 1 and ( maze[pos[0]][pos[1] + 1] or maze[pos[0]][pos[1] + 3] or maze[pos[0]][pos[1] + 5])== "X"):
            return True
        
        return False

    def apply_move(self, move):
        """This function applies the move to the original maze."""

        new_r, new_c = move
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] == self.player:
                    self.maze[r][c] = "."

        self.maze[new_r][new_c] = self.player
        self.player, self.opponent = self.opponent, self.player

    def get_winner(self, maze):
        """This function checks the winner of the game."""

        is_red_present = False
        is_green_present = False
        for r in maze:
            if "R" in r:
                is_red_present = True
            if "G" in r:
                is_green_present = True

        if not is_green_present or maze[9][19] == "R":
            return "Red wins!"
        if not is_red_present or maze[1][1] == "G":
            return "Green wins!"
        return "It's a draw!"

    def play(self):
        while not self.is_game_finished():
            if self.player == "R":
                best_move = self.minimax(self.maze, self.depth, True)[1]
            else:
                best_move = self.minimax(self.maze, self.depth, False)[1]

            if best_move:
                print("Player", self.player, "moves to:", best_move)
                self.apply_move(best_move)
                self.tried_moves.append(best_move)

        print(self.get_winner(self.maze))

# Representation of the given maze
maze = [
    ["X", "X", "X", "X", "X","X", "X", "X", "X", "X","X", "X", "X", "X", "X","X", "X", "X", "X", "X","X"],
    ["X", "R", "|", ".", "|",".", "|", ".", "|", ".","X", ".", "|", ".", "|",".", "|", ".", "|", ".","X"],
    ["X", "|", "X", "X", "X","X", "X", "|", "|", "|","X", "|", "|", "|", "|","|", "|", "|", "|", "|","X"],
    ["X", ".", "|", ".", "|",".", "|", ".", "|", ".","|", ".", "|", ".", "|",".", "|", ".", "|", ".","X"],
    ["X", "|", "|", "|", "|","|", "X", "X", "X", "|","|", "|", "X", "X", "X","|", "X", "|", "|", "|","X"],
    ["X", ".", "|", ".", "|",".", "X", ".", "|", ".","|", ".", "X", ".", "|",".", "X", ".", "|", ".","X"],
    ["X", "|", "X", "X", "X","|", "X", "|", "|", "|","X", "X", "X", "|", "|","|", "X", "|", "|", "|","X"],
    ["X", ".", "X", ".", "|",".", "|", ".", "|", ".","|", ".", "X", ".", "|",".", "|", ".", "|", ".","X"],
    ["X", "|", "X", "|", "|","|", "X", "X", "X", "|","|", "|", "X", "|", "X","X", "X", "X", "X", "X","X"],
    ["X", ".", "|", ".", "|",".", "|", ".", "|", ".","|", ".", "|", ".", "|",".", "|", ".", "|", "G","X"],
    ["X", "X", "X", "X", "X","X", "X", "X", "X", "X","X", "X", "X", "X", "X","X", "X", "X", "X", "X","X"],
]

Maze(maze).play()
