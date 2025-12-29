class MancalaBoard:
    """Représente l'état du plateau Mancala"""
    
    def __init__(self):
        # Dictionnaire: fosses A-F (player1), G-L (player2), magasins 1 et 2
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,
            '1': 0, # Magasin joueur 1
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,
            '2': 0
        }
        
        # Fosses de chaque joueur
        self.player1_pits = ('A', 'B', 'C', 'D', 'E', 'F')
        self.player2_pits = ('G', 'H', 'I', 'J', 'K', 'L')
        
        # Dictionnaire des fosses opposées
        self.opposite_pits = {
            'A': 'L', 'B': 'K', 'C': 'J', 'D': 'I', 'E': 'H', 'F': 'G',
            'G': 'F', 'H': 'E', 'I': 'D', 'J': 'C', 'K': 'B', 'L': 'A'
        }
        
        # Dictionnaire pour la séquence (sens inverse horaire)
        self.next_pit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'G', 'G': 'H', 'H': 'I', 'I': 'J', 'J': 'K', 'K': 'L',
            'L': '2', '2': 'A'
        }
    
    def possibleMoves(self, player): # retourne les mouvements possibles

        if player == 'player1':
            pits = self.player1_pits
        else:
            pits = self.player2_pits
        
        return [pit for pit in pits if self.board[pit] > 0] #retourne fosses avec pierres disponibles
    
    def doMove(self, player, pit): #execute un mouvement

        # Déterminer magasins
        my_store = '1' if player == 'player1' else '2'
        opponent_store = '2' if player == 'player1' else '1'

        my_pits = self.player1_pits if player == 'player1' else self.player2_pits #recupere fosses du joueur
        
        # Récupérer pierres
        stones = self.board[pit] #nombre de pierres dans la fosse choisie
        self.board[pit] = 0 #vider la fosse
        
        # Distribuer
        current = pit
        while stones > 0:
            current = self.next_pit[current] #prochaine fosse
            
            # Sauter magasin adversaire
            if current == opponent_store: #si cest le magasin adverse, je mis pas de pierre
                current = self.next_pit[current] #je passe a la fosse suivante
            
            self.board[current] += 1
            stones -= 1
        
        # Règle capture: dernière pierre dans fosse VIDE de mon côté

        if (current in my_pits and  # si la derniere pierre est dans mes fosses
            self.board[current] == 1 and  #jai une seule piere tsma li 9bl was 0 
            current in self.opposite_pits): #jai une fosse opposée(machi magasin)
            
            opposite = self.opposite_pits[current] #je recupere la fosse opposée
            if self.board[opposite] > 0: #si elle contient des pierres
                # Capturer
                self.board[my_store] += self.board[current] + self.board[opposite]
                self.board[current] = 0
                self.board[opposite] = 0
    
    def __str__(self):
        return f"""
        Player 2
  L    K    J    I    H    G
 {self.board['L']:2}   {self.board['K']:2}   {self.board['J']:2}   {self.board['I']:2}   {self.board['H']:2}   {self.board['G']:2}
{self.board['2']:2}                          {self.board['1']:2}
 {self.board['A']:2}   {self.board['B']:2}   {self.board['C']:2}   {self.board['D']:2}   {self.board['E']:2}   {self.board['F']:2}
  A    B    C    D    E    F
        Player 1
"""
