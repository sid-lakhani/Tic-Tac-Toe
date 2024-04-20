class MinimaxAI:
    def __init__(self, check_win_state_func):
        self.check_win_state = check_win_state_func

    def minimax(self, board, depth, is_maximizing):
        res = self.check_win_state(board)
        if res == 1:
            return 10 - depth
        elif res == -1:
            return -10 + depth
        elif res == 0:
            return 0
            
        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = -1
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = 0
                        best_score = min(score, best_score)
            return best_score

    def play_best_move(self, markers, place_marker_func):
        best_score = float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if markers[i][j] == 0:
                    markers[i][j] = -1
                    score = self.minimax(markers, 0, True)
                    markers[i][j] = 0
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            place_marker_func(best_move[0], best_move[1])
