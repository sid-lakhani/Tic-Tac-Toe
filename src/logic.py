class GameLogic:
    def __init__(self):
        self.reset()
        
    def reset(self, vs_ai=False):
        self.markers = [[0, 0, 0] for _ in range(3)]
        self.player = 1
        self.winner = 0
        self.game_over = False
        self.vs_ai = vs_ai

    def check_win_state(self, board):
        lines = list(board)
        lines.extend([[board[j][i] for j in range(3)] for i in range(3)])
        lines.append([board[i][i] for i in range(3)])
        lines.append([board[i][2 - i] for i in range(3)])
        
        for line in lines:
            if sum(line) == 3:
                return 1
            elif sum(line) == -3:
                return -1
                
        if all(cell != 0 for row in board for cell in row):
            return 0
        return None

    def update_winner(self):
        res = self.check_win_state(self.markers)
        if res is not None:
            self.winner = 1 if res == 1 else (2 if res == -1 else 0)
            self.game_over = True
            return True
        return False

    def place_marker(self, x, y):
        if self.markers[x][y] == 0 and not self.game_over:
            self.markers[x][y] = self.player
            self.player *= -1
            return True
        return False
