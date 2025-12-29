from Game import Game
from Play import Play

def main():
    print("=" * 60)
    print("    JEU MANCALA - MINIMAX ALPHA-BETA")
    print("=" * 60)
    
    print("\nChoisissez votre côté:")
    print("1. Player 1 (fosses A-F)")
    print("2. Player 2 (fosses G-L)")
    
    choice = input("Choix (1/2): ")
    
    if choice == '1':
        player_sides = {'HUMAN': 'player1', 'COMPUTER': 'player2'}
        current_player = 'player1'
    else:
        player_sides = {'HUMAN': 'player2', 'COMPUTER': 'player1'}
        current_player = 'player1'
    
    game = Game(player_sides)
    play = Play(game, depth=6)
    
    while not game.gameOver():
        print("\n" + "=" * 60)
        print(game.state)
        print("=" * 60)
        
        if current_player == player_sides['HUMAN']:
            play.humanTurn()
        else:
            play.computerTurn()
        
        current_player = 'player2' if current_player == 'player1' else 'player1'
    
    print("\n" + "=" * 60)
    print(game.state)
    print("=" * 60)
    print("\nFIN DU JEU!")
    
    winner, score_w, score_l = game.findWinner()
    if winner == 'DRAW':
        print(f"Match nul! {score_w} - {score_l}")
    else:
        print(f"Gagnant: {winner}")
        print(f"Score: {score_w} - {score_l}")
        print(f"Avantage: {score_w - score_l} pierres")

if __name__ == "__main__":
    main()
