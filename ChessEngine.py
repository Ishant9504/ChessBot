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
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        # A dictionary to map each piece type to its corresponding move function
        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }

        # White moves first
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
        moves = []
        for r in range(len(self.board)):  # Number of rows
            for c in range(len(self.board[r])):  # Number of columns in the current row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # Call the appropriate move function

        return moves

    """
    Get all the valid pawn moves for the pawn located at row, col. and add these moves to the list.
    Handles basic pawn movement and captures.
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # White pawn moves
            if self.board[r - 1][c] == "--":  # 1-square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2-square pawn advance (from starting position)
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # Capture to the left
                if self.board[r - 1][c - 1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # Capture to the right
                if self.board[r - 1][c + 1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # Black pawn moves
            if self.board[r + 1][c] == "--":  # 1-square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2-square pawn advance (from starting position)
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Capture to the left
                if self.board[r + 1][c - 1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # Capture to the right
                if self.board[r + 1][c + 1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    """
    Get all the valid rook moves for the rook located at row, col. and add these moves to the list.
    Handles vertical and horizontal movement until the rook encounters another piece or the edge of the board.
    """
    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Rook can move at most 7 squares in any direction
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if move is on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty space is a valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece is a valid capture
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break  # Stop looking in this direction after capturing
                    else:  # Friendly piece blocks the rook's movement
                        break
                else:  # Off the board
                    break

    """
    Get all the valid knight moves for the knight located at row, col. and add these moves to the list.
    Handles the L-shaped movement pattern of the knight.
    """
    def getKnightMoves(self, r, c, moves):
        knightMoves = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if move is on the board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Empty or enemy piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    """
    Get all the valid bishop moves for the bishop located at row, col. and add these moves to the list.
    Handles diagonal movement in all four diagonal directions.
    """
    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Top-left, top-right, bottom-left, bottom-right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Bishop can move at most 7 squares in any direction
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if move is on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty space is a valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece is a valid capture
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break  # Stop looking in this direction after capturing
                    else:  # Friendly piece blocks the bishop's movement
                        break
                else:  # Off the board
                    break

    """
    Get all the valid queen moves for the queen located at row, col. and add these moves to the list.
    Handles both diagonal and straight movement (combination of rook and bishop moves).
    """
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)  # Queen's straight moves (like a rook)
        self.getBishopMoves(r, c, moves)  # Queen's diagonal moves (like a bishop)

    """
    Get all the valid king moves for the king located at row, col. and add these moves to the list.
    Handles single-square movement in any direction.
    """
    def getKingMoves(self, r, c, moves):
        kingMoves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if move is on the board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Empty or enemy piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))

"""
This class represents a move in the chess game.
It stores the start and end positions of the move, the piece that was moved, and any piece that was captured.
"""
class Move:
    # Maps keys to values so that human-readable positions like (row, col) can be translated to chess notation like 'e4'
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
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
