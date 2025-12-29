import copy
from Game import Game

class Play:    
    def __init__(self, game, depth=6, heuristic='basic'):
        self.game = game
        self.depth = depth
        self.heuristic = heuristic
    
    def humanTurn(self):

        human_side = self.game.playerSide['HUMAN']
        moves = self.game.state.possibleMoves(human_side) #Fosses avec pierres possibles
        
        if not moves:
            return
        
        while True:
            choice = input("Fosse: ").upper() #Demande à l'utilisateur une fosse
            if choice in moves: #Vérifie si le choix est valide
                break #sort de la boucle si valide
            else:
             print("Invalide!")
        
        self.game.state.doMove(human_side, choice) #Exécute le coup choisi par l'utilisateur
    
    def computerTurn(self):

        computer_side = self.game.playerSide['COMPUTER']
        
        
        value, best_pit = self.MinimaxAlphaBetaPruning( #best move selon minimax
            self.game,
            Game.MAX,
            self.depth,
            float('-inf'),
            float('inf')
        )
        
        if best_pit is None:
            return
                
        self.game.state.doMove(computer_side, best_pit) #Exécute le meilleur coup trouvé
    
    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta):

        # Condition d'arrêt
        if game.gameOver() or depth == 1:
            bestValue = self.evaluateNode(game)
            return bestValue, None
        
        if player == Game.MAX:
            # MAX maximise
            bestValue = float('-inf')
            bestPit = None
            player_side = game.playerSide['COMPUTER']
            
            for pit in game.state.possibleMoves(player_side):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(player_side, pit)
                
                value, _ = self.MinimaxAlphaBetaPruning(child_game, -player, depth - 1, alpha, beta)
                
                if value > bestValue:
                    bestValue = value
                    bestPit = pit
                
                if bestValue >= beta:
                    break
                
                if bestValue > alpha:
                    alpha = bestValue
        
        else:
            # MIN minimise
            bestValue = float('inf')
            bestPit = None
            player_side = game.playerSide['HUMAN']
            
            for pit in game.state.possibleMoves(player_side):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(player_side, pit)
                
                value, _ = self.MinimaxAlphaBetaPruning(child_game, -player, depth - 1, alpha, beta)
                
                if value < bestValue:
                    bestValue = value
                    bestPit = pit
            
                if bestValue <= alpha:
                    break
                
                if bestValue < beta:
                    beta = bestValue
        
        return bestValue, bestPit
    
    def evaluateNode(self, game):

        if self.heuristic == 'advanced':
            return self.evaluateAdvanced(game)
        else:
            return game.evaluate()
    
    def evaluateAdvanced(self, game):

        computer_side = game.playerSide['COMPUTER']
        human_side = game.playerSide['HUMAN']
        
        computer_store = '1' if computer_side == 'player1' else '2'
        human_store = '1' if human_side == 'player1' else '2'
        
        computer_pits = game.state.player1_pits if computer_side == 'player1' else game.state.player2_pits
        human_pits = game.state.player1_pits if human_side == 'player1' else game.state.player2_pits
        
        store_diff = game.state.board[computer_store] - game.state.board[human_store] #difference des magasins

        mobility = len([p for p in computer_pits if game.state.board[p] > 0]) - \
                   len([p for p in human_pits if game.state.board[p] > 0]) # nombre de fosses plaines
        
        potential = sum(game.state.board[p] for p in computer_pits) - \
                    sum(game.state.board[p] for p in human_pits) # pierres totales dans les fosses
        
        return 10 * store_diff + 0.5 * mobility + 0.2 * potential
    
    #logique de l'heuristique 

    #jai des pieres dans mon magasin, et dans les fosses jai plus de pierres que ladversaire 
    #et jai plus de pierres totales dans mes fosses que ladversaire 
    #je valorise plus le magasin, puis la mobilite (fosses pleines)
    #puis le nombre total de pierres dans les fosses
