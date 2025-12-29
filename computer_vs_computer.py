from Game import Game
from Play import Play

def main():
    print("=" * 60)
    print("    MANCALA - ORDINATEUR VS ORDINATEUR")
    print("=" * 60)
    
    # Configuration: deux ordinateurs
    player_sides = {'COMPUTER': 'player1', 'HUMAN': 'player2'}
    
    game = Game(player_sides)
    
    # Deux IA avec profondeurs et heuristiques DIFFÉRENTES
    play1 = Play(game, depth=5, heuristic='advanced')  # Ordinateur 1 (plus profond, advanced)
    play2 = Play(game, depth=5, heuristic='basic')     # Ordinateur 2 (moins profond, basic)
    
    current_player = 'player1'
    turn_count = 0
    
    print("\nOrdinateur 1 (player1, depth=8, advanced) vs Ordinateur 2 (player2, depth=5, basic)")
    
    while not game.gameOver():
        turn_count += 1
        print(f"\n{'=' * 60}")
        print(f"Tour {turn_count}: {current_player}")
        print(game.state)
        print("=" * 60)
        
        if current_player == 'player1':
            # Ordinateur 1 avec heuristique avancée et profondeur 8
            computer_side = 'player1'
            value, best_pit = play1.MinimaxAlphaBetaPruning(
                game, Game.MAX, 8, float('-inf'), float('inf')
            )
            print(f"Ordinateur 1 (advanced, depth=8) joue: {best_pit} (valeur: {value})")
            game.state.doMove(computer_side, best_pit)
        else:
            # Ordinateur 2 avec heuristique basique et profondeur 5 - utilise MIN
            computer_side = 'player2'
            
            value, best_pit = play2.MinimaxAlphaBetaPruning(
                game, Game.MAX, 5, float('-inf'), float('inf')
            )
            print(f"Ordinateur 2 (basic, depth=5, MIN) joue: {best_pit} (valeur: {value})")
            game.state.doMove(computer_side, best_pit)
        
        current_player = 'player2' if current_player == 'player1' else 'player1'
    
    print("\n" + "=" * 60)
    print(game.state)
    print("=" * 60)
    print("\nFIN DU JEU!")
    print(f"Nombre de tours: {turn_count}")
    
    # Résultats
    score1 = game.state.board['1']
    score2 = game.state.board['2']
    
    if score1 > score2:
        print(f"\nGagnant: Ordinateur 1 (advanced)")
        print(f"Score: {score1} - {score2}")
        print(f"Avantage: {score1 - score2} pierres")
    elif score2 > score1:
        print(f"\nGagnant: Ordinateur 2 (basic)")
        print(f"Score: {score2} - {score1}")
        print(f"Avantage: {score2 - score1} pierres")
    else:
        print(f"\nMatch nul! {score1} - {score2}")

if __name__ == "__main__":
    main()
