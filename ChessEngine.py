"""
This class is responsible for storing the information for the current State of the game and
determining the valid moves at the current state and also keeps a move log.
"""

class GameState:
    def __init__(self):
        # The board is an 8x8 2D list
        # First character represents the color of the piece: 'w' for white, 'b' for black
        # Second character represents the type of the piece: 'R', 'N', 'B', 'Q', 'K', 'p'
        # "--" represents an empty tile
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bp", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True

        # A list to keep track of the moves made, allowing for undo functionality
        self.moveLog = []

        # Track the king's position for both players, important for check conditions
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

    """
    Takes a move as a parameter and executes it.
    Updates the board, logs the move, and switches the turn.
    This implementation does not handle castling, en passant, or promotion.
    """
    def makeMove(self, move):
        # Move the piece to the new location
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        # Log the move so it can be undone later
        self.moveLog.append(move)

        # Swap players: white to move -> black to move, and vice versa
        self.whiteToMove = not self.whiteToMove

        # Update king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    """
    Undo the last move made. This method pops the last move from the move log and reverts the board to the previous state.
    """
    def undoMove(self):
        if len(self.moveLog) != 0:  # Ensure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # Switch turns back

            # Update king's position back to the original if the king was moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    """
    Generate all valid moves for the current player, considering checks.
    """
    def getValidMoves(self):
        # 1. Generate all possible moves without considering checks
        moves = self.getAllPossibleMoves()
        # 2. Iterate through each move and simulate the move
        for i in range(len(moves) - 1, -1, -1):  # Iterate backward when removing from the list
            self.makeMove(moves[i])
            # 3. Generate all opponent's moves and check if any attacks the current player's king
            # 4. Undo the move (to revert back to original state)
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])# 5. If the move leaves the king in check, it's not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        return moves

    """
    Determine if the current player's king is in check.
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    """ 
    Determine if enemy can attack the square r, c
    """

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove# switch to opponent's move
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove# switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:# square is under attack
                return True
        return False

    """
    Generate all possible moves for the current player without considering checks.
    """
    def getAllPossibleMoves(self):
        pass


class Move():
    # map keys to values
    # key: values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + self.endCol

    '''
    Overriding equal methods
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

        # Assign a move ID to uniquely identify each move, useful for undo functionality and debugging
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """
    Overriding the equals method to allow easy comparison between moves.
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    """
    Converts the move into chess notation (e.g., 'e2e4') by translating row and column indices.
    """
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    """
    Converts row and column into human-readable chess coordinates like 'e4'.
    """
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
