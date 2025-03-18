import networkx as nx
import matplotlib.pyplot as plt
import random

class GameState:
    def __init__(self, stones, player_turn, player_score, opponent_score):
        self.stones = stones  # Akmeņu skaits uz galda
        self.player_turn = player_turn  # Kurš spēlē (True - cilvēks, False - dators)
        self.player_score = player_score  # Spēlētāja punkti
        self.opponent_score = opponent_score  # Pretinieka punkti
        self.children = []  # Iespējamie gājieni (apakšmezgli)
        self.value = None  # Stāvokļa novērtējums (Minimakss / Alfa-beta algoritms)

def generate_game_tree(state, depth=0, max_depth=30, max_children=2):
    if state.stones == 0:
        # Ja spēle beigusies, aprēķinām punktus
        final_score = state.player_score + (0 if state.player_turn else state.stones)
        opponent_final = state.opponent_score + (state.stones if state.player_turn else 0)
        state.value = final_score - opponent_final  # Stāvokļa novērtējums
        return state
    
    if depth >= max_depth:
        return state  # Nepārsniedzam maksimālo dziļumu

    possible_moves = [2, 3]
   # random.shuffle(possible_moves)  # Lai dažādotu spēles gājienus
    
    selected_moves = possible_moves[:max_children]  # Izvēlamies ierobežotu gājienu skaitu
    
    for move in selected_moves:
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
            state.children.append(generate_game_tree(next_state, depth + 1, max_depth, max_children))

    return state

# var izņemt ārā
def visualize_tree(root):
    """Vizualizē spēles koku hierarhiskā struktūrā ar papildu atstarpēm un marķējumu līdz 0."""
    graph = nx.DiGraph()
    pos = {}
    
    def add_edges(state, parent=None, level=0, x=0, y=0, width=6.0):
        node_label = f"{state.stones} | P1: {state.player_score} | P2: {state.opponent_score}"
        pos[node_label] = (x, -y * 2)  # Paplašinām vertikālo atstarpi
        graph.add_node(node_label)
        if parent:
            graph.add_edge(parent, node_label)
        
        num_children = len(state.children)
        step = width / max(num_children, 1)
        next_x = x - (width / 2) + (step / 2)
        
        for i, child in enumerate(state.children):
            add_edges(child, node_label, level + 1, next_x + i * step, y + 1, width / 1.5)
    
    add_edges(root, x=0, y=0)
    
    plt.figure(figsize=(18, 14))  # Palielinām attēla izmēru
    nx.draw(graph, pos, with_labels=True, node_size=2500, node_color='lightblue', font_size=8, edge_color='gray')
    plt.show()

# Spēles koka ģenerēšanas piemērs 50 akmeņiem
initial_state = GameState(stones=50, player_turn=True, player_score=0, opponent_score=0)
game_tree = generate_game_tree(initial_state, max_depth=10, max_children=2)

# Vizualizējam koku
visualize_tree(game_tree)