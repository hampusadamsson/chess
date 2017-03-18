from Cell import Cell
from termcolor import colored
import sys
import copy
import random

# STATE SPACE REPRESENTATION
# 64 cells
# each cell:  
#  team - 1
#  type - 5
class Chess:

    #
    # constructor
    #
    def __init__(self):
        self.board = []
        self.init_b()
        self.init_p()

    #
    # init board
    #
    def init_b(self):
        self.board = []
        for a in range(64):
            tmp = Cell()
            self.board.append(tmp)

    #
    # init pieces
    #
    def init_p(self):
        pos = [8,48]
        for o in pos:
            for x in range(o, o+8):
                self.board[x].unit[0] = 1
                self.board[x].unit[1] = o>30
                self.board[x].unit[2] = 1
                self.board[x].set_type()
                
        pos = [0,56]
        for o in pos:
            for x in range(o, o+8):
                self.board[x].unit[0] = 1
                self.board[x].unit[1] = o>30
                if x<(o+5):
                    self.board[x].unit[(x+2)%7+1] = 1
                else:
                    self.board[x].unit[4-(x+2)%7+1] = 1
                self.board[x].set_type()

    #
    # print all units
    #
    def p_b(self):
        for c in self.board:
            print c.unit
            
    #
    # print board - human readable
    #
    def human_r(self):
        print "-"
        print "0 1 2 3 4 5 6 7"
        for x in range(8):
            tmp = []
            for y in range(8):
                if self.get_cell(x, y).is_empty():
                    col = "grey"
                    typ = "0"
                else:
                    typ = self.get_cell(x, y).get_type()
                    team = self.get_cell(x, y).get_team()
                    if team==0:
                        col = "red"
                    else:
                        col = "blue"
                sys.stdout.write(colored(typ+" ",col))
            print x

    #
    # Return cell at x,y - coordinates
    # INVERTED!
    #
    def get_cell(self, x, y):
        return self.board[(x*8)+y]

    #
    # Gives cell based on input
    #
    def inp_cell(self):
        try:
            inp = str(input())        
            if len(inp)==1:
                inp='0'+inp
            
            y = int(inp[0])
            x = int(inp[1])
            p = self.get_cell(x,y)
            return p,x,y
        except:
            return 0,0,0
    
    #
    # check if team is check
    #
    def check(self, team):
        for x in range(8):
            for y in range(8):
                p = self.get_cell(y,x)
                if p!=0 and p.is_empty()==False and p.get_team()!=team:
                    p_m = p.options(self.board,x,y)
                    for (x2,y2) in p_m:
                        t = self.get_cell(y2,x2)
                        if t.get_type()=="K" and t.get_team()==team:
                            return True
        return False

    #
    # check if check
    #
    def is_check(self):
        w = self.check(0)
        b = self.check(1)
        return (w,b)

    #
    # make pawn->queen
    #
    def make_q(self,p,y):
        # print p.get_type()
        if p.get_type()=="p":
            if y==0 or y==7:
                p.unit[2], p.unit[6] = p.unit[6], p.unit[2]
                p.set_type()
    #
    # try move
    #
    def move(self,p,t,team,x,y):
        t2 = copy.deepcopy(t)
        p2 = copy.deepcopy(p)
        self.move_perform(p,t)

        # revert if still check
        if self.check(team)==True:
            self.move_perform(t2,t)
            self.move_perform(p2,p)
            return False

        # make queen if needed
        self.make_q(t,y)
            
        return True


    #
    # can move?
    #
    def can_move(self,team):
        for x in range(8):
            for y in range(8):
                p = self.get_cell(y,x)
                if p!=0 and p.is_empty()==False and p.get_team()==team:
                    p_m = p.options(self.board,x,y)
                    for (x2,y2) in p_m:
                        t = self.get_cell(y2,x2)
                        t2 = copy.deepcopy(t)
                        p2 = copy.deepcopy(p)
                        if self.move(p,t,team,x2,y2):
                            self.move_perform(t2,t)
                            self.move_perform(p2,p)
                            return True
        return False
    
    #
    # check if mate
    #
    def is_mate(self,team):
        for x in range(8):
            for y in range(8):
                p = self.get_cell(y,x)
                if p!=0 and p.is_empty()==False and p.get_team()==team:
                    pos_move = p.options(self.board,x,y)
                    for (x2,y2) in pos_move:
                        t = self.get_cell(y2,x2)
                        t2 = copy.deepcopy(t)
                        p2 = copy.deepcopy(p)
                        if self.move(p,t,team,x2,y2):
                            self.move_perform(t2,t)
                            self.move_perform(p2,p)
                            return False
        return True
                
    #
    # Perform a move between prev -> new
    #
    def move_perform(self, prev, new):
        new.unit = copy.deepcopy(prev.unit)
        new.set_type()
        prev.clear()

    #
    # draw
    #
    def draw(self):
        pieces=0
        for x in range(8):
            for y in range(8):
                p = self.get_cell(y,x)
                if p!=0 and p.is_empty()==False:
                    pieces+=1
        if pieces==2:
            return True
        return False
            
    #
    # random play - get random piece
    #
    def get_random(self, team):
        pos = []
        for x in range(8):
            for y in range(8):
                p = self.get_cell(y,x)
                if p.get_team()==team and p.is_empty() == False:
                    pos.append((p,x,y))
        return random.choice(pos)

    #
    # debug class
    #
    def king_die(self):
        kings=0
        for x in range(8):
            for y in range(8):
                p = self.get_cell(y,x)
                if p!=0 and p.is_empty()==False:
                    if self.get_cell(y,x).get_type() == 'K':
                        kings+=1
        if kings==2:
            return True
        return False
    
    #
    # Play automatically
    #
    def auto_play(self):
        col = {0:"white",1:"black"}
        turn = 0
        b_mate = 0
        w_mate = 0
        mate = [0,0]
        
        while(mate[0]==mate[1]):
            # print col.get(turn), "turn"

            res = self.is_check()
            
            # draw control
            if res[0]==res[1]:
                if self.draw() or self.can_move(turn)==False:
                    return res

            # check control
            for x in [0,1]:
                if res[x]==1:
                    # print col.get(x),"in check"
                    if self.is_mate(x):
                        mate[x]=1
                        return res
                
            # move this piece
            p,x,y = self.get_random(turn)

            # move to this cell
            pos_move = p.options(self.board,x,y)

            # check if move is viable
            x2,y2 = -1,-1
            while (x2,y2) not in pos_move:
                if len(pos_move)==0:
                    break
                x2,y2 = random.choice(pos_move)
                t = self.get_cell(y2,x2)

            # swap piece if no possible moves
            if len(pos_move)==0:
                continue
            
            # perform move
            if self.move(p,t,turn,x2,y2)==False:
                continue

            # print board
            self.human_r()
            print x,y,"->",x2,y2

            # breaks if a king died
            if not self.king_die():
                print "KING DIED!",x,y,t.unit,pos_move,self.is_check()
                exit() # error

            # change turn            
            turn+=1
            turn=turn%2

    
    # #
    # # play game
    # #
    # def play(self):
    #     turn = 0 #white start
    #     b_mate = 0
    #     w_mate = 0
        
    #     while(b_mate==w_mate):
    #         if turn:
    #             print "Black turn"
    #         else:
    #             print "White turn"

    #         print "Move from:"
    #         # move this piece
    #         p,y,x = self.inp_cell()
            
    #         # checks that its a valid cell
    #         if p == 0:
    #             print "invalid cell"
    #             continue
    #         elif p.is_empty():
    #             print "empty piece"
    #             continue
    #         elif p.get_team() != turn:
    #             print "not your piece"
    #             continue

    #         # move to this cell
    #         pos_move = p.options(self.board,x,y)

    #         # check if move is viable
    #         x2,y2 = -1,-1
    #         while (y2, x2) not in pos_move:
    #             print pos_move
    #             print "Move to:"
    #             t,x2,y2 = self.inp_cell()
    #             if t==0 or len(pos_move)==0:
    #                 break
    #         if t==0 or len(pos_move)==0:
    #             continue
            
    #         # perform move
    #         # if self.move(p,t,turn)==False:
    #         #     x,y,"->",x2,y2
    #         #     continue
            
    #         # print board
    #         self.human_r()
    #         # change turn

    #         # check control
    #         w, b = self.is_check()
    #         if w:
    #             print "White in CHECK!"
    #         if b:
    #             print "Black in CHECK!"
                
    #         turn+=1
    #         turn=turn%2

            



wins = [0,0]

for x in range(10):
    b = Chess()
    b_win,w_win = b.auto_play()
    wins[0]+=b_win
    wins[1]+=w_win

print wins

b.human_r()
