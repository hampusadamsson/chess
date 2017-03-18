from Cell import Cell

# STATE SPACE REPRESENTATION
# 64 cells to play
# each cell = team, type
#

class Board:

    def __init__(self):
        self.cells = []
        self.init_board()
        self.init_pieces()

    def init_board(self):
        for x in range(8):
            for y in range(8):
                tmp = Cell()
                tmp.name = chr(65 + x) + str(y + 1)
                tmp.pos = [x, y]
                self.cells.append(tmp)

    def init_pieces(self):
        for team in range(2):
            for x in range(2):
                t = "pawn"
                for y in range(8):
                    if x == team:
                        if y == 0 or y == 7:
                            t = "rook"
                        elif y == 1 or y == 6:
                            t = "horse"
                        elif y == 2 or y == 5:
                            t = "bishop"
                        elif y == 3:
                            t = "king"
                        elif y == 4:
                            t = "queen"

                    new_p = cr_p(t, self.board[(team * 6 + x) % 8][y][0], team)
                    self.pieces.append(new_p)


#    def disp_p(self):
#        for p in self.pieces:
#            print p.name + "-" + p.pos + "-" + str(p.team)


game = Board()
#game.disp_p()