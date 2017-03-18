


class Cell:

    #
    # Constructor
    # unit - 7 ints
    # 1-bit   = contains piece (1=piece)
    # 2-bit   = team
    # 3-7 bit = 2-pawn, 4-knight, 5-bishop, 3-rook, 6-queen, 7-king
    #
    def __init__(self):
        self.unit = [0,0,0,0,0,0,0,0]
    
    #
    # Returns the team of the piece
    #
    def get_team(self):
        return self.unit[1]

    # Returns if cell is empty
    #
    def is_empty(self):
        return self.unit[0]==0
    
    #
    # 'Kills' piece
    #
    def clear(self):
        self.unit = [0]*len(self.unit)

    #
    # Return the piece type
    # return 0 if no piece
    #
    def get_type(self):
        if self.unit[2]:   #pawn
            return 'p'#1
        elif self.unit[3]: #rook
            return 'R'#2
        elif self.unit[4]: #knight
            return 'k'#3
        elif self.unit[5]: #bishop
            return 'B'#4
        elif self.unit[6]: #queen
            return 'Q'#5
        elif self.unit[7]: #king
            return 'K'#6
        else:
            return '0'

    #
    # set movement function for piece
    #
    def set_type(self):
        if self.unit[2]:   #pawn
            self.move_func = self.pawn
        elif self.unit[3]: #rook
            self.move_func = self.rook
        elif self.unit[4]: #knight
            self.move_func = self.knight
        elif self.unit[5]: #bishop
            self.move_func = self.bishop
        elif self.unit[6]: #queen
            self.move_func = self.queen
        elif self.unit[7]: #king
            self.move_func = self.king
        else:
            return '0'
    
    #
    # return a list with potential moves
    #
    def options(self,board,x,y):
        typ = self.get_type()
        self.moves = self.move_func(board,x,y)
        self.clear_invalid_moves()
        return self.moves

    #
    # Removes invalid moves from move-list
    #
    def clear_invalid_moves(self):
        tmp_moves = []
        for (x,y) in self.moves:
            if x>=0 and x<=7:
                if y>=0 and y<=7:
                    tmp_moves.append((x,y))
        self.moves = tmp_moves
    
    #
    # pawn movement
    #
    def pawn(self,board,x,y):
        moves = []
        if self.get_team():
            y2=-1
        else:
            y2=1
        
        # move forward if empty
        if get_cell(board,x,y+y2)!=0 and get_cell(board,x,y+y2).is_empty():
            moves.append((x,y+y2))
            if (y==1 and self.get_team()==0) or (y==6 and self.get_team()==1):
                if get_cell(board,x,y+(2*y2)).is_empty():
                    moves.append((x,y+(2*y2)))
                    
        # take foe if possible
        if get_cell(board,x+1,y+y2)!=0 and get_cell(board,x+1,y+y2).is_empty()==False:
            if get_cell(board,x+1,y+y2).get_team()!=self.get_team():
                moves.append((x+1,y+y2))

        # take foe if possible
        if get_cell(board,x-1,y+y2)!=0 and get_cell(board,x-1,y+y2).is_empty()==False:
            if get_cell(board,x-1,y+y2).get_team()!=self.get_team():
                moves.append((x-1,y+y2))
        
        return moves

    #
    # bishop
    #
    def bishop(self,board,x,y):
        moves = []

        tmp = range(x-8,x)
        tmp.reverse()
        
        ranges = [range(x+1,8), tmp]
        for ran in ranges:
            for t_x in ran:
                p = get_cell(board, t_x,y+t_x-x)

                if p == 0:
                    break
                elif p.is_empty():
                    moves.append((t_x,y+t_x-x))
                elif p.get_team()!=self.get_team():
                    moves.append((t_x,y+t_x-x))
                    break
                else:
                    break

        ranges = [range(x+1,8), tmp]
        for ran in ranges:
            for t_x in ran:
                p = get_cell(board, t_x,y-t_x+x)

                if p == 0:
                    break
                elif p.is_empty():
                    moves.append((t_x,y-t_x+x))
                elif p.get_team()!=self.get_team():
                    moves.append((t_x,y-t_x+x))
                    break
                else:
                    break
        return moves

    #
    # rook
    #
    def rook(self,board,x,y):
        moves = []

        tmp = range(x-8,x)
        tmp.reverse()
        
        ranges = [range(x+1,8), tmp]
        for ran in ranges:
            for t_x in ran:
                p = get_cell(board, t_x, y)
                if p.is_empty():
                    moves.append((t_x,y))
                elif p.get_team()!=self.get_team():
                    moves.append((t_x,y))
                    break
                else:
                    break

        tmp = range(x-8,y)
        tmp.reverse()
        ranges = [range(y+1,8), tmp]
        for ran in ranges:
            for t_y in ran:
                p = get_cell(board, x, t_y)
                if p.is_empty():
                    moves.append((x,t_y))
                elif p.get_team()!=self.get_team():
                    moves.append((x,t_y))
                    break
                else:
                    break
        return moves

    #
    # knight
    #
    def knight(self,board,x,y):
        moves = []
        final_move = []
        
        moves.append((x+2,y+1))
        moves.append((x+2,y-1))
        moves.append((x-2,y+1))
        moves.append((x-2,y-1))
        moves.append((x+1,y+2))
        moves.append((x-1,y+2))
        moves.append((x+1,y-2))
        moves.append((x-1,y-2))

        for m in moves:
            # take foe if possible
            if m[0]<0 or m[0]>7 or m[1]<0 or m[1]>7:
                continue
            pc = get_cell(board,m[0],m[1])
            if pc.get_team()!=self.get_team() or pc.is_empty():
                final_move.append(m)
        return final_move

    #
    # king
    #
    def king(self,board,x,y):
        moves = []
        for t_x in range(-1,2):
            for t_y in range(-1,2):
                if t_x==0 and t_y==0:
                    continue

                p = get_cell(board,x+t_x,y+t_y)
                
                if p==0:
                    moves.append((x+t_x, y+t_y))
                    # continue
                elif p.is_empty():
                    moves.append((x+t_x, y+t_y))
                elif p.get_team()!=get_cell(board,x,y).get_team():
                    moves.append((x+t_x, y+t_y))
        return moves

    #
    # queen
    #
    def queen(self,board,x,y):
        m1 = self.bishop(board,x,y)
        m2 = self.rook(board,x,y)
        moves = m1+m2
        return moves

#
# Return cell at x,y - coordinates
#
def get_cell(board, x, y):
    try:
        return board[(y*8)+x]
    except:
        return 0
