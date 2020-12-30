"""
Tic Tac Toe Player
"""

from copy import deepcopy

X, O = "X", "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cells = [ele for row in board for ele in row]
    return X if cells.count(X) <= cells.count(O) else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("InvalidMove")
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]

        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[1][1] != EMPTY:
        return board[1][1]

    if board[0][2] == board[1][1] == board[2][0] and board[1][1] != EMPTY:
        return board[1][1]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return all([board[i][j] for i in range(3) for j in range(3)]) or winner(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)
    if won == X:
        return 1
    if won == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board
    using Alpha-Beta Pruning algorithm
    """
    if terminal(board):
        return None
    if player(board) == X:
        return maximize(board)[1]
    else:
        return minimize(board)[1]


def maximize(state):
    if terminal(state):
        return utility(state), None
    value, best_move = float("-inf"), None
    for action in actions(state):
        tmp = minimize(result(state, action))[0]
        if tmp >= value:
            value = tmp
            best_move = action
            if value == 1:
                return value, best_move
    return value, best_move


def minimize(state):
    if terminal(state):
        return utility(state), None
    value, best_move = float("inf"), None
    for action in actions(state):
        tmp = maximize(result(state, action))[0]
        if tmp <= value:
            value = tmp
            best_move = action
            if value == -1:
                return value, best_move
    return value, best_move
