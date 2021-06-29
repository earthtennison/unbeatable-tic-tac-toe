import copy


class TicTacToe:
    def __init__(self):
        self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.last_player = ''
        self.turn_played = 0

    def play(self, player, index):
        row = (index - 1) // 3
        col = (index - 1) % 3

        # check player name
        if player not in ['O', 'X']:
            print("invalid player name.")
            return False
        # check is slot empty
        elif self.board[row][col] in ['O', 'X']:
            print("invalid slot.")
            return False

        # place
        else:
            self.board[row][col] = player
            self.last_player = player
            self.turn_played += 1
            return True

    def is_game_over(self):
        if any([self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2] for i in range(3)]) or \
                any([self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] for i in \
                     range(3)]) or \
                self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] or \
                self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2]:
            # print(f"{self.last_player} wins")
            return self.last_player
        elif self.turn_played == 9:
            # print("draws")
            return 'D'
        else:
            return False

    def display(self):
        """
        display board
        ------------
        | 1 | 2 | 3 |
        ------------
        | 4 | 5 | 6 |
        ------------
        | 7 | 8 | 9 |
        ------------

        :return:
        """
        slot = ""
        for i in range(3):
            print("-" * 13)
            slot += "| "
            for j in range(3):
                slot += str(self.board[i][j]) + " | "
            print(slot)
            slot = ""

        print("-" * 13)

    def get_empty_slot(self):
        slot = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] not in ['O', 'X']:
                    slot.append(self.board[i][j])
        return slot


def minimax(game, is_max_turn, is_current_game, alpha, beta):
    global count
    winner = game.is_game_over()
    if not winner == False:
        count += 1

        # return score = number of slot left when game is over + 1.
        # if com wins sign is +, else -
        # if draws, score = 0

        # O is com
        if winner == 'O':
            return + (10 - game.turn_played)
        elif winner == 'X':
            return - (10 - game.turn_played)
        elif winner == 'D':
            return 0
    else:
        if is_max_turn:
            max_score = -10
            best_index = 0
            for i in game.get_empty_slot():
                # com forecast
                game_copy = copy.deepcopy(game)
                if game_copy.play('O', i):
                    score = minimax(game_copy, False, False, alpha, beta)
                    if score > max_score:
                        max_score = score
                        best_index = i
                    #alpha-beta pruning
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            # return the best slot only for the current game not forecast game
            if is_current_game == True:
                return best_index
            return max_score

        else:
            min_score = 10
            for i in game.get_empty_slot():
                # player forecast
                game_copy = copy.deepcopy(game)
                if game_copy.play('X', i):
                    score = minimax(game_copy, True, False, alpha, beta)
                    if score < min_score:
                        min_score = score

                    #alpha-beta pruning
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return min_score


if __name__ == "__main__":
    game = TicTacToe()
    print("UNBEATABLE TIC TAC TOE\nby Thanachot (Earth) Sappakit\n")
    print("Type a number from 1-9")
    game.display()
    player = ''
    while True:
        player = input("\nwho go first?\nyou[X] or computer[O] :")
        if player not in ['O','X','o','x']:
            print("invalid input")
            continue
        else:
            player = player.upper()
            break
    count = 0

    while not game.is_game_over():
        if player == 'O':
            index = minimax(game, True, True, -10, 10)
            print(f"computer found {count} possibilities")
            print(f"computer (O) play at {index}")
            count = 0
        else:
            index = (input(f"player {player} select: "))
            if not index.isnumeric():
                print("invalid input")
                continue
            index = int(index)

        if game.play(player, index):
            game.display()
            player = 'X' if player == 'O' else 'O'

    if game.is_game_over() in ['O','X']:
        print(f"{game.is_game_over()} wins")
    else:
        print("draws")