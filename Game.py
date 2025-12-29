from MancalaBoard import MancalaBoard

class Game:
    
    MAX = 1   # COMPUTER
    MIN = -1  # HUMAN
    
    def __init__(self, player_sides=None):
        self.state = MancalaBoard()
        if player_sides is None:
            self.playerSide = {'COMPUTER': 'player1', 'HUMAN': 'player2'}
        else:
            self.playerSide = player_sides
    
    def gameOver(self):
#on recupere nb pierres dans les fosses de chaque joueur et on verifie si cest 0 donc vide
        player1_empty = all(self.state.board[p] == 0 for p in self.state.player1_pits)
        player2_empty = all(self.state.board[p] == 0 for p in self.state.player2_pits) 
        
        if player1_empty:
            for pit in self.state.player2_pits:
                self.state.board['2'] += self.state.board[pit] #On recupère les pierres restantes dans le magasin '2'
                self.state.board[pit] = 0 #On vide les fosses tous 
            return True
        
        if player2_empty:
            for pit in self.state.player1_pits:
                self.state.board['1'] += self.state.board[pit]
                self.state.board[pit] = 0
            return True
        
        return False
    
    def findWinner(self):

        computer_store = '1' if self.playerSide['COMPUTER'] == 'player1' else '2'
        human_store = '1' if self.playerSide['HUMAN'] == 'player1' else '2'
        
        computer_score = self.state.board[computer_store] #On recupère nb piere du magasin de l'ordi
        human_score = self.state.board[human_store] #On recupère le score du joueur humain
        
        if computer_score > human_score:
            return 'COMPUTER', computer_score, human_score
        elif human_score > computer_score:
            return 'HUMAN', human_score, computer_score
        else:
            return 'DRAW', computer_score, human_score
    
    def evaluate(self):

        #Heuristique: différence magasins

        computer_store = '1' if self.playerSide['COMPUTER'] == 'player1' else '2'
        human_store = '1' if self.playerSide['HUMAN'] == 'player1' else '2'
        return self.state.board[computer_store] - self.state.board[human_store]
