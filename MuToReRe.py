class Case :

    def __init__(self,id,color):
        self.id = id
        self.color = color

class Board :

    def __init__(self):
        self.current = [[Case(7,'w'),Case(8,'w'),Case(9,'w')],[Case(4,'w'),Case(5,'o'),Case(6,'b')],[Case(1,'b'),Case(2,'b'),Case(3,'b')]]
        self.neighbors = [(4,2),(1,3),(2,6),(1,7),None,(3,9),(4,8),(7,9),(6,8)]
        self.turn = 'b'

    def nextTurn(self):
    	if self.turn == 'b' :
    		self.turn = 'w'
    	else :
    		self.turn = 'b'

    def show(self):
        for row in self.current :
            print(row[0].color + ' ' + row[1].color + ' ' + row[2].color)

    def checkNeighbors(self,id):
    	return not (self.searchCaseById(self.neighbors[id-1][0]).color == self.searchCaseById(self.neighbors[id-1][1]).color and self.searchCaseById(self.neighbors[id-1][0]).color == self.searchCaseById(id).color)


    def searchCaseById(self,id):
    	for row in self.current :
    		for case in row :
    			if case.id == id :
    				return case


    def checkMove(self,player,id):

    	if not (id < 10 and id > 0):
    		return False

    	case = self.searchCaseById(id)

    	if id != 5 :
    		neighbors = (self.searchCaseById(self.neighbors[id-1][0]),self.searchCaseById(self.neighbors[id-1][1]))

    	if player != self.turn :
    		return False

    	if player != case.color :
    		return False

    	if case.id != 5 :
    		if not self.checkNeighbors(case.id) :
    			return False

    	if id != 5 :
	    	if self.current[1][1].color != 'o' and neighbors[0].color != 'o' and neighbors[1].color != 'o' :
	    		return False

    	return True


    def checkEndConditions(self,player):
    	canMove = False
    	for i in range(1,10) :
    		canMove |= self.checkMove(player,i)
    	return canMove

    def move(self,id):

        case = self.searchCaseById(id)
        if id != 5 :
        	neighbors = (self.searchCaseById(self.neighbors[id-1][0]),self.searchCaseById(self.neighbors[id-1][1]))


        	if self.current[1][1].color == 'o' :
        		self.current[1][1].color = case.color
        		case.color = 'o'

        	elif neighbors[0].color == 'o':
        		neighbors[0].color = case.color
        		case.color = 'o'

        	elif neighbors[1].color == 'o' :
        		neighbors[1].color = case.color
        		case.color = 'o'

        else :
        	for row in self.current :
        		for a in row :
        			if a.id != 5 and a.color == 'o' :
        				a.color = case.color
        				case.color = 'o'



# Création d'un jeu de Mu Torere à deux joueurs


if __name__ == "__main__" :
    board = Board()
    print("Etat initial :")
    board.show()

    playing = True
    player = 'b'

    turn = 0

    while(playing):
        if player == 'b' :
            nextMove = int(input("Black can choose his next move : "))
        else :
            nextMove = int(input("White can choose his next move : "))
        
        isValid = board.checkMove(player,nextMove)

        if isValid :
            board.move(nextMove)
            board.nextTurn()
            if player == 'b':
            	player = 'w'
            else :
            	player = 'b'

            turn += 1
            print()
            print("Tour n°" + str(turn))
            board.show()
            print()

        else :
            print("This move is not allowed. Please choose another one.")

        if not board.checkEndConditions(player) :
            if player == 'b' :
                winner = "White"
            else :
                winner = 'Black'
            print()
            print(winner + " won the game !")
            input("Press any key to exit the game")
            playing = False


