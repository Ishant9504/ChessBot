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
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False


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

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'


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
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  #only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                #To block a check you must move a piece into one of the squares between the enemy and the kind
                check = self.checks[0]  #Check Information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]  #enemy piece causing check
                validSquares = []  #Squares that piece can move to

                #if knight must capture knight or move king
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (
                        kingRow + check[2] * i, kingCol + check[3] * i)  #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:  #oce you get to piece and checks
                            break
                #get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1,
                               -1):  #go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != "K":  #move doesn't move king so it must block or capture
                        if not (moves[i].endRow,
                                moves[i].endCol) in validSquares:  #move doesn't block check or capture piece
                            moves.remove(moves[i])

            else:  #double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else:  #not in check so all moves are fine
            moves = self.getAllPossibleMoves()

        return moves
        # # 1. Generate all possible moves without considering checks
        # moves = self.getAllPossibleMoves()
        # # 2. Iterate through each move and simulate the move
        # for i in range(len(moves) - 1, -1, -1):  # Iterate backward when removing from the list
        #     self.makeMove(moves[i])
        #     # 3. Generate all opponent's moves and check if any attacks the current player's king
        #     # 4. Undo the move (to revert back to original state)
        #     self.whiteToMove = not self.whiteToMove
        #     if self.inCheck():
        #         moves.remove(moves[i])# 5. If the move leaves the king in check, it's not a valid move
        #     self.whiteToMove = not self.whiteToMove
        #     self.undoMove()
        #
        # if len(moves) == 0:# either checkmate or stalemate
        #     if self.inCheck():
        #         self.checkMate = True
        #     else:
        #         self.staleMate = True
        # else:
        #     self.checkMate = False
        #     self.staleMate = False
        # return moves

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
        self.whiteToMove = not self.whiteToMove  # switch to opponent's move
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True
        return False

    """
    Generate all possible moves for the current player without considering checks.
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in given row
                piece = self.board[r][c]
                if piece != "--":  # Skip empty squares
                    turn = piece[0]
                    if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                        pieceType = piece[1]
                        self.moveFunctions[pieceType](r, c,
                                                      moves)  # Calls the appropriate move function based on piece type
        return moves

    '''
    Returns if the player is in check, a list of pins and a list of checks
    '''

    def checkForPinsAndChecks(self):
        pins = []  #squares where the allied pinned piece is and direction pinned from
        checks = []  #squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        #Check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  #reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():  #1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  #2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        #5 possibilities in this complex conditional
                        #1.) orthogonally away from king and piece is a rook
                        #2.) diagonally away from king and piece is a bishop
                        #3.) 1 square away diagonally from king and piece is pawn
                        #4.) any direction and piece is queen
                        #5.) any direction 1 square away and piece is a king( this is necessary to prevent a kinf move to square controlled by another king)
                        if (0 <= j <= 3 and type == "R") or \
                                (4 <= j <= 7 and type == "B") or \
                                (i == 1 and type == "p" and (
                                        (enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
                                (type == "Q") or (i == 1 and type == "K"):
                            if possiblePin == ():  #No piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  #piece blocking so pin
                                pins.append(possiblePin)
                        else:  #enemy piece not applying check
                            break

                else:
                    break  #off board
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":  # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    """
    Get all the valid pawn moves for the pawn located at row, col. and add these moves to the list.
    Handles basic pawn movement and captures.
    """

    def getPawnMoves(self, row, col, moves):
        '''
        Get all the pawn moves for the pawn located at row, col and add the moves to the list.
        '''
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:  # white pawn moves
            if self.board[row - 1][col] == "--":  # 1 square pawn advance
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((row, col), (row - 1, col), self.board))  # (start square, end square, board)
                    if row == 6 and self.board[row - 2][col] == "--":  # 2 square pawn advance
                        moves.append(Move((row, col), (row - 2, col), self.board))

            if col - 1 >= 0:  # capturing to the left - impossible if a pawn is standing in a far left column
                if self.board[row - 1][col - 1][0] == "b":  # enemy piece to capture
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))

            if col + 1 <= 7:  # capturing to the right - analogical
                if self.board[row - 1][col + 1][0] == "b":  # enemy piece to capture
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:  # black pawn moves
            if self.board[row + 1][col] == "--":  # 1 square pawn advance
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(Move((row, col), (row + 2, col), self.board))

            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == "w":
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))

            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == "w":
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def getRookMoves(self, row, col, moves):
        '''
        Get all the rook moves for the rook located at row, col and add the moves to the list.
        '''
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][
                    1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getKnightMoves(self, row, col, moves):
        '''
        Get all the knight moves for the knight located at row col and add the moves to the list.
        '''
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))  # up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.whiteToMove else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # so it's either enemy piece or empty square
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def getBishopMoves(self, row, col, moves):

        '''
        Get all the bishop moves for the bishop located at row col and add the moves to the list.
        '''
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getQueenMoves(self, row, col, moves):
        '''
        Get all the queen moves for the queen located at row col and add the moves to the list.
        '''
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        '''
        Get all the king moves for the king located at row col and add the moves to the list.
        '''
        row_moves = (-1, -1, -1, 0, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 0, 1, -1, 0, 1)
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.whiteKingLocation = (end_row, end_col)
                    else:
                        self.blackKingLocation = (end_row, end_col)
                    in_check, pins, checks = self.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)


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
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True

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
