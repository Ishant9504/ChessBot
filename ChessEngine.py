"""
This class is responsible for storing the information for the current State of the game and
determining the valid moves at current state and also keeps a move log
"""
class GameState():
    def __init__(self):
        #The board is 8x8 2D list
        #First Character represents colour of piece 'w' or 'b'
        #Second Character represents type of piece 'R','N','B','Q' or 'K'
        #"--" represent empty tile
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whiteToMove = True
        self.moveLog = []
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the moves so we can undo it later
        self.whiteToMove =  not self.whiteToMove #swap players
class Move():
    # map keys to values
    # key: values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
    colToFiles = {v: k for k,v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        #can be turned into real chess notation
        return self.getRankFile(self.startRow, self.startCol) +self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colToFiles[c] + self.rowsToRanks[r]
