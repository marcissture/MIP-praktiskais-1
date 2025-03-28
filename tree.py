class GameState:
    def __init__(self, stones, player_turn, player_score, computer_score, player_stones=0, computer_stones=0):
        self.stones = stones  # Akmeņu skaits uz galda
        self.player_turn = player_turn  # True - cilvēks, False - dators
        self.player_score = player_score  # Cilvēka punkti
        self.computer_score = computer_score  # Datora punkti
        self.player_stones = player_stones  # Cilvēka paņemtie akmeņi
        self.computer_stones = computer_stones  # Datora paņemtie akmeņi
        self.children = []  # Iespējamie gājieni (apakšmezgli)
        # Stāvokļa novērtējums (priekš Minimaksa / Alfa-beta)
        self.value = None

    def is_terminal(self):
        """Pārbauda, vai stāvoklis ir galējs (spēle beigusies)"""
        # Spēle beidzas, kad uz galda ir 0 vai 1 akmens (jo nevar paņemt 1 akmeni)
        return self.stones < 2

    def calculate_final_score(self):
        """Aprēķina galīgos punktus spēles beigās"""
        final_player_score = self.player_score + self.player_stones
        final_computer_score = self.computer_score + self.computer_stones

        if final_player_score > final_computer_score:
            return "Uzvar cilvēks!"
        elif final_computer_score > final_player_score:
            return "Uzvar dators!"
        else:
            return "Neizšķirts!"

    def evaluate(self):
        """Heiristiskā novērtējuma funkcija spēles stāvoklim"""
        if self.is_terminal():
            # Termināla stāvoklim aprēķinām faktisko vērtību
            final_player_score = self.player_score + self.player_stones
            final_computer_score = self.computer_score + self.computer_stones
            # Pozitīva vērtība nozīmē labumu datoram
            return final_computer_score - final_player_score

        # Pamata komponentes novērtējumā
        score_diff = self.computer_score - self.player_score
        stones_diff = self.computer_stones - self.player_stones

        # Novērtējam gājiena priekšrocību
        turn_value = 0
        if not self.player_turn:  # Datora gājiens
            turn_value = 3  # Datora gājiens ir labvēlīgs datoram
        else:
            turn_value = -3  # Cilvēka gājiens nav labvēlīgs datoram

        # Novērtējam paritātes kontroli
        parity_control = 0
        stones_left = self.stones

        # Ja uz galda ir 2 vai 3 akmeņi, un ir datora gājiens, tas ir ļoti izdevīgi
        if stones_left in [2, 3] and not self.player_turn:
            parity_control = 30
        # Ja uz galda ir 4 vai 5 akmeņi, un ir cilvēka gājiens, tas ir izdevīgi datoram
        elif stones_left in [4, 5] and self.player_turn:
            parity_control = 20

        # Stratēģija atkarībā no atlikušo akmeņu skaita
        stones_strategy = 0

        # Ja akmentiņu skaits ir starp 6 un 12, mēģinām analizēt modulo 5 paritāti
        if 6 <= stones_left <= 12:
            # Ja atlikušais skaits % 5 == 0 vai % 5 == 1, tas parasti ir izdevīgi spēlētājam, kura gājiens nav
            if stones_left % 5 in [0, 1]:
                stones_strategy = 10 if self.player_turn else -10
            # Ja atlikušais skaits % 5 == 2 vai % 5 == 3 vai % 5 == 4, tas parasti ir izdevīgi spēlētājam, kura gājiens ir
            else:
                stones_strategy = -10 if self.player_turn else 10

        # Galējā posma stratēģija (mazāk nekā 10 akmeņu)
        endgame_strategy = 0
        if stones_left < 10:
            # Atkarībā no tā, cik akmeņu atlicis, izvērtējam situāciju
            if (stones_left - 2) % 5 == 0 or (stones_left - 3) % 5 == 0:
                endgame_strategy = 15 if not self.player_turn else -15

        # Aprēķinām kopējo novērtējumu
        evaluation = (
            score_diff * 2 +        # Punktu starpība (ar koeficientu)
            stones_diff * 1 +       # Akmeņu starpība
            turn_value +            # Gājiena priekšrocība
            parity_control +        # Paritātes kontrole
            stones_strategy +       # Akmeņu skaita stratēģija
            endgame_strategy        # Gala posma stratēģija
        )

        return evaluation


def generate_game_tree(state, depth=0, max_depth=3):
    """Ģenerē spēles koku ar noteiktu dziļumu"""
    # Aprēķinām heiristisko novērtējumu šim stāvoklim
    state.value = state.evaluate()

    # Pārbaudam, vai esam sasnieguši gala stāvokli
    if state.is_terminal():
        return state

    # Pārbaudam, vai esam sasnieguši maksimālo dziļumu
    if depth >= max_depth:
        return state

    possible_moves = [2, 3]  # Iespējamie gājieni

    for move in possible_moves:
        if state.stones >= move:
            # Kopējam esošos datus
            new_stones = state.stones - move
            new_player_score = state.player_score
            new_computer_score = state.computer_score
            new_player_stones = state.player_stones
            new_computer_stones = state.computer_stones

            # Atjaunojam akmentiņu skaitu, ko katrs spēlētājs paņēmis
            if state.player_turn:
                new_player_stones += move
            else:
                new_computer_stones += move

            # Pievienojam punktus atkarībā no atlikušo akmeņu paritātes
            if new_stones % 2 == 0:  # Pāra skaits
                if state.player_turn:
                    new_computer_score += 2  # Punkti datoram
                else:
                    new_player_score += 2  # Punkti cilvēkam
            else:  # Nepāra skaits
                if state.player_turn:
                    new_player_score += 2  # Punkti cilvēkam
                else:
                    new_computer_score += 2  # Punkti datoram

            # Izveidojam jaunu mezglu un turpinām koka ģenerāciju
            next_state = GameState(
                new_stones,
                not state.player_turn,
                new_player_score,
                new_computer_score,
                new_player_stones,
                new_computer_stones
            )

            # Ģenerējam apakškoku šim stāvoklim
            child_state = generate_game_tree(next_state, depth + 1, max_depth)
            state.children.append(child_state)

    return state


def minimax(state, depth, is_maximizing):
    """
    Minimax algorithm for game decision making.

    Parameters:
    state (GameState): Current game state
    depth (int): Current depth in the game tree
    is_maximizing (bool): True if maximizing player (computer), False if minimizing (player)

    Returns:
    tuple: (best_state, best_value) - The best state to move to and its value
    """
    # Base case: if state is terminal or we've reached maximum depth
    if state.is_terminal() or depth == 0 or not state.children:
        return state, state.value

    # Computer's turn (maximizing)
    if is_maximizing:
        best_value = float('-inf')
        best_state = None

        for child in state.children:
            _, value = minimax(child, depth - 1, False)

            if value > best_value:
                best_value = value
                best_state = child

        return best_state, best_value

    # Player's turn (minimizing)
    else:
        best_value = float('inf')
        best_state = None

        for child in state.children:
            _, value = minimax(child, depth - 1, True)

            if value < best_value:
                best_value = value
                best_state = child

        return best_state, best_value


def alpha_beta(state, depth, alpha, beta, is_maximizing):
    """
    Alpha-Beta pruning algorithm for game decision making.

    Parameters:
    state (GameState): Current game state
    depth (int): Current depth in the game tree
    alpha (float): Alpha value for pruning
    beta (float): Beta value for pruning
    is_maximizing (bool): True if maximizing player (computer), False if minimizing (player)

    Returns:
    tuple: (best_state, best_value) - The best state to move to and its value
    """
    # Base case: if state is terminal or we've reached maximum depth
    if state.is_terminal() or depth == 0 or not state.children:
        return state, state.value

    # Computer's turn (maximizing)
    if is_maximizing:
        best_value = float('-inf')
        best_state = None

        for child in state.children:
            _, value = alpha_beta(child, depth - 1, alpha, beta, False)

            if value > best_value:
                best_value = value
                best_state = child

            alpha = max(alpha, best_value)

            # Pruning condition
            if beta <= alpha:
                break

        return best_state, best_value

    # Player's turn (minimizing)
    else:
        best_value = float('inf')
        best_state = None

        for child in state.children:
            _, value = alpha_beta(child, depth - 1, alpha, beta, True)

            if value < best_value:
                best_value = value
                best_state = child

            beta = min(beta, best_value)

            # Pruning condition
            if beta <= alpha:
                break

        return best_state, best_value


# Update the computer_move function to use these algorithms properly
def computer_move(state, algorithm, max_depth=3):
    """Datora gājiena izpilde"""
    # Ģenerējam koku no pašreizējā stāvokļa
    game_tree = generate_game_tree(state, 0, max_depth)

    # Izvēlamies gājienu, balstoties uz algoritmu
    if algorithm == "minimax":
        # True because computer is maximizing
        best_child, _ = minimax(game_tree, max_depth, True)
    else:  # alpha-beta
        best_child, _ = alpha_beta(
            game_tree, max_depth, float('-inf'), float('inf'), True)

    return best_child  # Return the best state to move to


def player_move(state, stones_to_take):
    """Cilvēka gājiena izpilde"""
    # Pārbaudam, vai gājiens ir spēkā
    if stones_to_take not in [2, 3] or stones_to_take > state.stones:
        return state

    # Izpildām gājienu
    new_stones = state.stones - stones_to_take
    new_player_score = state.player_score
    new_computer_score = state.computer_score

    # Atjaunojam spēlētāja paņemtos akmeņus
    new_player_stones = state.player_stones + stones_to_take

    # Pievienojam punktus atkarībā no atlikušo akmeņu paritātes
    if new_stones % 2 == 0:  # Pāra skaits
        new_computer_score += 2  # Punkti datoram
    else:  # Nepāra skaits
        new_player_score += 2  # Punkti spēlētājam

    new_state = GameState(
        new_stones,
        False,  # Tagad datora gājiens
        new_player_score,
        new_computer_score,
        new_player_stones,
        state.computer_stones
    )

    return new_state
