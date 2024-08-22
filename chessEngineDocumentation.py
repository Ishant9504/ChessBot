"""
Chess Game Engine

This module is responsible for handling the game state, move generation, and move execution for a simple chess game.
It includes classes to manage the game board, determine valid moves, and log the move history.

Classes:
    GameState: Manages the state of the chess game, including the board configuration, player turns, and move history.
    Move: Represents a move in the chess game, including the start and end positions, and any pieces captured.

"""

class GameState:
    """
    A class to represent the state of a chess game.

    Attributes:
        board (list): A 2D list representing the 8x8 chess board. Each element is a string representing a chess piece or an empty square.
        moveFunctions (dict): A dictionary mapping piece types ('p', 'R', 'N', 'B', 'Q', 'K') to their respective move-generating methods.
        whiteToMove (bool): A boolean flag indicating whether it is white's turn to move.
        moveLog (list): A list of all moves that have been executed in the game.
        whiteKingLocation (tuple): A tuple representing the current location of the white king on the board.
        blackKingLocation (tuple): A tuple representing the current location of the black king on the board.

    Methods:
        makeMove(move): Executes a given move and updates the game state.
        undoMove(): Undoes the last move made, restoring the previous game state.
        getValidMoves(): Generates and returns all valid moves considering the current board state and checks.
        inCheck(): Determines whether the current player is in check. (Not implemented)
        getAllPossibleMoves(): Generates and returns all possible moves without considering checks.
        getPawnMoves(r, c, moves): Adds all valid pawn moves for the pawn at position (r, c) to the list of moves.
        getRookMoves(r, c, moves): Adds all valid rook moves for the rook at position (r, c) to the list of moves.
        getKnightMoves(r, c, moves): Adds all valid knight moves for the knight at position (r, c) to the list of moves.
        getBishopMoves(r, c, moves): Adds all valid bishop moves for the bishop at position (r, c) to the list of moves.
        getQueenMoves(r, c, moves): Adds all valid queen moves for the queen at position (r, c) to the list of moves.
        getKingMoves(r, c, moves): Adds all valid king moves for the king at position (r, c) to the list of moves.
    """

    def __init__(self):
        """
        Initializes the GameState with a standard 8x8 chess board setup, white to move, and an empty move log.
        """
        # The board is an 8x8 2D list. Each element is a string representing a piece ('bR', 'wK', etc.) or "--" for empty.
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
        # A dictionary to map piece types to their respective move generation methods
        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }
        self.whiteToMove = True  # White moves first
        self.moveLog = []  # Logs all moves for undo functionality
        self.whiteKingLocation = (7, 4)  # Track the white king's position
        self.blackKingLocation = (0, 4)  # Track the black king's position

    def makeMove(self, move):
        """
        Executes a move, updates the board, and switches the turn to the other player.

        Args:
            move (Move): The move to be executed.
        """
        self.board[move.startRow][move.startCol] = "--"  # Empty the start square
        self.board[move.endRow][move.endCol] = move.pieceMoved  # Place the piece on the end square
        self.moveLog.append(move)  # Log the move for later reference
        self.whiteToMove = not self.whiteToMove  # Switch turns

        # Update king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        """
        Undoes the last move made, restoring the previous game state.
        """
        if len(self.moveLog) != 0:  # Ensure there is a move to undo
            move = self.moveLog.pop()  # Remove the last move from the log
            self.board[move.startRow][move.startCol] = move.pieceMoved  # Move the piece back
            self.board[move.endRow][move.endCol] = move.pieceCaptured  # Restore the captured piece
            self.whiteToMove = not self.whiteToMove  # Switch turns back

            # Update king's location if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        """
        Generates and returns a list of all valid moves for the current player, considering checks.

        Returns:
            list: A list of Move objects representing valid moves.
        """
        # TODO: Implement check and checkmate detection
        moves = self.getAllPossibleMoves()

        # For each move, temporarily make the move, check if it leaves the king in check, and undo the move
        for i in range(len(moves) - 1, -1, -1):  # Iterate backward to safely remove elements
            self.makeMove(moves[i])
            # Generate all opponent's moves and check if any of them attack the king
            self.undoMove()

        # TODO: Remove moves that place the player in check
        return moves

    def inCheck(self):
        """
        Checks if the current player's king is in check.
        """
        # TODO: Implement check detection logic
        pass

    def getAllPossibleMoves(self):
        """
        Generates and returns a list of all possible moves for the current player, without considering checks.

        Returns:
            list: A list of Move objects representing all possible moves.
        """
        moves = []
        for r in range(len(self.board)):  # Iterate over all rows
            for c in range(len(self.board[r])):  # Iterate over all columns in a row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # Call appropriate move function based on piece type

        return moves

    def getPawnMoves(self, r, c, moves):
        """
        Adds all valid pawn moves for the pawn at position (r, c) to the list of moves.

        Args:
            r (int): The row index of the pawn.
            c (int): The column index of the pawn.
            moves (list): The list of valid moves to be populated.
        """
        if self.whiteToMove:  # White pawn moves
            if self.board[r - 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # Capture to the left
                if self.board[r - 1][c - 1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # Capture to the right
                if self.board[r - 1][c + 1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # Black pawn moves
            if self.board[r + 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Capture to the left
                if self.board[r + 1][c - 1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # Capture to the right
                if self.board[r + 1][c + 1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        """
        Adds all valid rook moves for the rook at position (r, c) to the list of moves.

        Args:
            r (int): The row index of the rook.
            c (int): The column index of the rook.
            moves (list): The list of valid moves to be populated.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Friendly piece invalid
                        break
                else:  # Off board
                    break

    def getKnightMoves(self, r, c, moves):
        """
        Adds all valid knight moves for the knight at position (r, c) to the list of moves.

        Args:
            r (int): The row index of the knight.
            c (int): The column index of the knight.
            moves (list): The list of valid moves to be populated.
        """
        knightMoves = [
            (-2, -1), (-1, -2), (-2, 1), (-1, 2),
            (2, -1), (1, -2), (2, 1), (1, 2)
        ]
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Not an ally piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        """
        Adds all valid bishop moves for the bishop at position (r, c) to the list of moves.

        Args:
            r (int): The row index of the bishop.
            c (int): The column index of the bishop.
            moves (list): The list of valid moves to be populated.
        """
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal movements
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Bishops can move 1 to 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Friendly piece invalid
                        break
                else:  # Off board
                    break

    def getQueenMoves(self, r, c, moves):
        """
        Adds all valid queen moves for the queen at position (r, c) to the list of moves.

        Args:
            r (int): The row index of the queen.
            c (int): The column index of the queen.
            moves (list): The list of valid moves to be populated.
        """
        # Queen's moves are a combination of rook and bishop moves
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        """
        Adds all valid king moves for the king at position (r, c) to the list of moves.

        Args:
            r (int): The row index of the king.
            c (int): The column index of the king.
            moves (list): The list of valid moves to be populated.
        """
        kingMoves = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Not an ally piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move:
    """
    A class to represent a move in the chess game.

    Attributes:
        startRow (int): The row index of the starting square.
        startCol (int): The column index of the starting square.
        endRow (int): The row index of the ending square.
        endCol (int): The column index of the ending square.
        pieceMoved (str): The piece that was moved, represented as a string (e.g., 'wP' for white pawn).
        pieceCaptured (str): The piece that was captured, represented as a string (e.g., 'bQ' for black queen).
        moveID (int): A unique identifier for the move, useful for comparison and debugging.

    Methods:
        __eq__(other): Checks if two Move objects are equal based on their moveID.
        getChessNotation(): Converts the move into standard chess notation (e.g., 'e2e4').
        getRankFile(r, c): Converts a row and column index into human-readable chessboard coordinates (e.g., 'e4').
    """

    # Maps for converting between rows/columns and chess notation
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        """
        Initializes a Move object with the start and end squares, and the pieces involved.

        Args:
            startSq (tuple): The starting square as a tuple (row, col).
            endSq (tuple): The ending square as a tuple (row, col).
            board (list): The current state of the chess board.
        """
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # A unique identifier for the move, created by combining the start and end positions
        self.moveID = (self.startRow * 1000 + self.startCol * 100 +
                       self.endRow * 10 + self.endCol)

    def __eq__(self, other):
        """
        Checks if two Move objects are equal based on their moveID.

        Args:
            other (Move): The other move to compare with.

        Returns:
            bool: True if the moves are equal, False otherwise.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        """
        Converts the move into standard chess notation.

        Returns:
            str: The move in chess notation (e.g., 'e2e4').
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        """
        Converts a row and column index into human-readable chessboard coordinates.

        Args:
            r (int): The row index.
            c (int): The column index.

        Returns:
            str: The coordinate in standard chess notation (e.g., 'e4').
        """
        return self.colsToFiles[c] + self.rowsToRanks[r]

