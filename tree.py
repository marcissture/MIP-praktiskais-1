class GameState:
    def __init__(self, stones, player_turn, player_score, opponent_score):
        self.stones = stones  # Akmeņu skaits uz galda
        self.player_turn = player_turn  # Kurš spēlē (True - cilvēks, False - dators)
        self.player_score = player_score  # Spēlētāja punkti
        self.opponent_score = opponent_score  # Pretinieka punkti
        self.children = []  # Iespējamie gājieni (apakšmezgli)
        self.value = None  # Stāvokļa novērtējums (Minimakss / Alfa-beta algoritms)

def generate_game_tree(state, depth=0, max_depth=10):
    if state.stones == 0 or depth >= max_depth:
        # Ja spēle beigusies vai sasniegts maksimālais dziļums, aprēķinām punktus
        final_score = state.player_score + (0 if state.player_turn else state.stones)
        opponent_final = state.opponent_score + (state.stones if state.player_turn else 0)
        state.value = final_score - opponent_final  # Stāvokļa novērtējums
        return state

    for move in [2, 3]:  # Iespējamie gājieni (paņemt 2 vai 3 akmeņus)
        if state.stones >= move:
            new_stones = state.stones - move
            new_player_score = state.player_score
            new_opponent_score = state.opponent_score

            # Nosakām, kuram pievieno punktus
            if new_stones % 2 == 0:
                new_opponent_score += 2  # Punkti pretiniekam
            else:
                new_player_score += 2  # Punkti spēlētājam

            # Izveidojam jaunu mezglu un turpinām koka ģenerāciju
            next_state = GameState(
                new_stones, not state.player_turn, new_player_score, new_opponent_score
            )
            state.children.append(generate_game_tree(next_state, depth + 1, max_depth))

    return state

# Spēles koka ģenerēšanas piemērs 10 akmeņiem
initial_state = GameState(stones=10, player_turn=True, player_score=0, opponent_score=0)
game_tree = generate_game_tree(initial_state, max_depth=5)

# Izvadām pirmā līmeņa iespējamos gājienus
for child in game_tree.children:
    print(child)
