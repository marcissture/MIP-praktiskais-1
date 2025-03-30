import tkinter as tk
from PIL import ImageTk, Image
from tree import GameState, generate_game_tree, player_move, computer_move
import matplotlib.pyplot as plt
import networkx as nx


class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Akmentini")
        self.root.geometry("375x667")
        self.create_bg()
        self.create_ctrl()
        self.game_state = None  # Sākotnēji spēles stāvoklis nav iestatīts
        self.algorithm = "minimax"  # Noklusējuma algoritms
        self.max_depth = 3  # Noklusējuma dziļums
        self.player_starts = True  # Noklusējuma vērtība - cilvēks sāk
        self.show_tree = False  # Vai rādīt koku kad dators domā
        self.total_nodes = 0  # Kopējais mezglu skaits visai spēlei
        self.total_time = 0.0  # Kopējais datora domāšanas laiks

    def clrscr(self):
        """Notīra ekrānu, saglabājot fona attēlu"""
        for widget in self.canvas.find_all():
            if widget != 1:  # 1 is typically the background image ID
                self.canvas.delete(widget)

    def create_bg(self):
        """Izveido fona attēlu"""
        bg_image = Image.open("bin/background.png").resize((375, 667))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas = tk.Canvas(self.root, width=375, height=667)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def create_ctrl(self):
        """Izveido sākuma ekrāna kontroles"""
        title_image = Image.open("bin/Akmentiņi.png").resize((187, 50))
        self.title_photo = ImageTk.PhotoImage(title_image)
        self.canvas.create_image(
            187, 80, image=self.title_photo, anchor="center")

        # Akmeņu skaita izvēle
        self.count = tk.IntVar(value=50)
        self.canvas.create_text(
            187, 150, text="Sākotnējais akmeņu skaits:", fill="white", font=("Arial", 12))

        left_img = Image.open("bin/left.png").resize((50, 50))
        self.left_photo = ImageTk.PhotoImage(left_img)
        right_img = Image.open("bin/right.png").resize((50, 50))
        self.right_photo = ImageTk.PhotoImage(right_img)

        left_btn = tk.Button(self.root, image=self.left_photo,
                             borderwidth=0, command=self.ctr_decrease, bg="black")
        right_btn = tk.Button(self.root, image=self.right_photo,
                              borderwidth=0, command=self.ctr_increase, bg="black")

        self.canvas.create_window(150, 240, window=left_btn)
        self.canvas.create_window(225, 240, window=right_btn)

        label = tk.Label(self.root, textvariable=self.count, font=(
            "Arial", 40, "bold"), bg="black", fg="white", width=5)
        self.canvas.create_window(187, 190, window=label)

        # Algoritma izvēle
        self.alg_var = tk.StringVar(value="minimax")
        self.canvas.create_text(
            187, 280, text="Algoritms:", fill="white", font=("Arial", 12))

        mm_rb = tk.Radiobutton(self.root, text="Minimaksa", variable=self.alg_var, value="minimax",
                               bg="black", fg="white", selectcolor="gray", font=("Arial", 10))
        ab_rb = tk.Radiobutton(self.root, text="Alfa-beta", variable=self.alg_var, value="alpha-beta",
                               bg="black", fg="white", selectcolor="gray", font=("Arial", 10))

        self.canvas.create_window(125, 310, window=mm_rb)
        self.canvas.create_window(250, 310, window=ab_rb)

        # Koka dziļuma izvēle
        self.depth_var = tk.IntVar(value=3)
        self.canvas.create_text(
            187, 340, text="Koka dziļums:", fill="white", font=("Arial", 12))

        depth_frame = tk.Frame(self.root, bg="black")
        for i in range(1, 6):
            rb = tk.Radiobutton(depth_frame, text=str(i), variable=self.depth_var, value=i,
                                bg="black", fg="white", selectcolor="gray", font=("Arial", 10))
            rb.pack(side=tk.LEFT, padx=5)

        self.canvas.create_window(187, 370, window=depth_frame)

        # Koka vizualizācijas izvēle
        self.tree_var = tk.BooleanVar(value=False)
        tree_cb = tk.Checkbutton(self.root, text="Rādīt spēles koku", variable=self.tree_var,
                                 bg="black", fg="white", selectcolor="gray", font=("Arial", 10))
        self.canvas.create_window(187, 400, window=tree_cb)

        # Spēlētāja izvēle
        self.player_var = tk.BooleanVar(value=True)
        self.canvas.create_text(
            187, 430, text="Kurš sāk?", fill="white", font=("Arial", 12))

        human_rb = tk.Radiobutton(self.root, text="Cilvēks", variable=self.player_var, value=True,
                                  bg="black", fg="white", selectcolor="gray", font=("Arial", 10))
        comp_rb = tk.Radiobutton(self.root, text="Dators", variable=self.player_var, value=False,
                                 bg="black", fg="white", selectcolor="gray", font=("Arial", 10))

        self.canvas.create_window(125, 460, window=human_rb)
        self.canvas.create_window(250, 460, window=comp_rb)

        # Pogas
        start_img = Image.open("bin/start.png").resize((150, 50))
        self.start_photo = ImageTk.PhotoImage(start_img)
        start_btn = tk.Button(self.root, image=self.start_photo,
                              borderwidth=0, command=self.start_game, bg="black")

        exit_img = Image.open("bin/exit.png").resize((150, 50))
        self.exit_photo = ImageTk.PhotoImage(exit_img)
        exit_btn = tk.Button(self.root, image=self.exit_photo,
                             borderwidth=0, command=self.exit_game, bg="black")

        self.canvas.create_window(187, 510, window=start_btn)
        self.canvas.create_window(187, 570, window=exit_btn)

    def ctr_increase(self):
        """Palielina akmeņu skaitu"""
        if self.count.get() < 70:
            self.count.set(self.count.get() + 1)

    def ctr_decrease(self):
        """Samazina akmeņu skaitu"""
        if self.count.get() > 50:
            self.count.set(self.count.get() - 1)

    def start_game(self):
        """Sāk spēli ar izvēlētiem parametriem"""
        self.clrscr()
        self.algorithm = self.alg_var.get()
        self.max_depth = self.depth_var.get()
        self.show_tree = self.tree_var.get()
        self.player_starts = self.player_var.get()

        # Iestatām sākuma stāvokli
        self.game_state = GameState(
            stones=self.count.get(),
            player_turn=self.player_starts,
            player_score=0,
            computer_score=0
        )

        self.update_game_display()

        # Ja sāk dators, uzreiz izpildām datora gājienu
        if not self.player_starts:
            self.root.after(500, self.make_computer_move)

    def exit_game(self):
        """Iziet no spēles"""
        self.root.destroy()

    def update_game_display(self):
        """Atjaunina spēles ekrānu, balstoties uz pašreizējo stāvokli"""
        self.clrscr()

        # Virsraksts
        self.canvas.create_text(
            187, 50, text="AKMEŅU SPĒLE", fill="white", font=("Arial", 24, "bold"))

        # Spēles statistika - vienkāršota versija
        self.canvas.create_text(187, 100, text=f"Akmeņi uz galda: {self.game_state.stones}",
                                fill="white", font=("Arial", 18, "bold"))

        self.canvas.create_text(187, 140, text=f"Cilvēks: {self.game_state.player_score} punkti, {self.game_state.player_stones} akmeņi",
                                fill="white", font=("Arial", 14))

        self.canvas.create_text(187, 170, text=f"Dators: {self.game_state.computer_score} punkti, {self.game_state.computer_stones} akmeņi",
                                fill="white", font=("Arial", 14))

        # Kārtējais gājiens
        turn_text = "Jūsu gājiens" if self.game_state.player_turn else "Datora gājiens"
        self.canvas.create_text(187, 210, text=turn_text,
                                fill="yellow" if self.game_state.player_turn else "cyan",
                                font=("Arial", 16, "bold"))

        # Poga atgriezties uz sākuma ekrānu
        exit_btn = tk.Button(self.root, text="Atgriezties uz sākumu", command=self.new_game,
                             bg="red", fg="white", font=("Arial", 12))
        self.canvas.create_window(187, 570, window=exit_btn)

        # Ja spēle beigusies, rādām rezultātu
        if self.game_state.is_terminal():
            self.show_game_over()
            return

        # Vienkāršotas pogas gājienu veikšanai (tikai cilvēka gājienam)
        if self.game_state.player_turn:
            # Poga "Paņemt 2 akmeņus"
            if self.game_state.stones >= 2:
                take_2_btn = tk.Button(self.root, text="Paņemt 2 akmeņus", command=lambda: self.make_player_move(2),
                                       bg="blue", fg="white", font=("Arial", 14))
                self.canvas.create_window(187, 300, window=take_2_btn)

            # Poga "Paņemt 3 akmeņus"
            if self.game_state.stones >= 3:
                take_3_btn = tk.Button(self.root, text="Paņemt 3 akmeņus", command=lambda: self.make_player_move(3),
                                       bg="green", fg="white", font=("Arial", 14))
                self.canvas.create_window(187, 350, window=take_3_btn)

    def make_player_move(self, stones_to_take):
        """Izpilda cilvēka gājienu"""
        if not self.game_state.player_turn:
            return

        # Pārbaudam, vai gājiens ir derīgs
        if stones_to_take not in [2, 3] or stones_to_take > self.game_state.stones:
            return


        self.game_state = player_move(self.game_state, stones_to_take)

        self.update_game_display()

        # Ja spēle nav beigusies un tagad ir datora gājiens
        if not self.game_state.is_terminal() and not self.game_state.player_turn:
            # Izmantojam after, lai dotu laiku interfeisam atjaunoties
            self.root.after(1000, self.make_computer_move)

    def make_computer_move(self):
        """Izpilda datora gājienu"""
        if self.game_state.player_turn:
            return

        # Ģenerējam koku spēles stāvoklim
        game_tree = generate_game_tree(
            self.game_state, max_depth=self.max_depth)

        # Ja izvēlēts rādīt koku, parādām to
        if self.show_tree:
            self.visualize_tree(
                game_tree, f"Spēles koks - Datora gājiens (dziļums: {self.max_depth})")

        # Izpildām datora gājienu
        next_state = computer_move(
            self.game_state, self.algorithm, self.max_depth)

        # Iegūstam metrikas no pēdējā gājiena
        metrics = getattr(next_state, "metrics", {})
        node_count = metrics.get("node_count", 0)
        duration = metrics.get("duration", 0.0)

        self.total_nodes += node_count
        self.total_time += duration

        self.game_state = next_state
        # Atjauninām ekrānu
        self.update_game_display()

    def visualize_tree(self, root, title="Spēles koks"):
        """Vizualizē spēles koku hierarhiskā struktūrā"""
        graph = nx.DiGraph()
        pos = {}

        def add_edges(state, parent=None, level=0, x=0, y=0, width=6.0):
            # Izveidojam mezgla etiķeti ar visiem parametriem, ieskaitot heiristisko vērtību
            node_label = (f"Stones: {state.stones} | "
                          f"Turn: {'Player' if state.player_turn else 'Computer'}\n"
                          f"Player: {state.player_score}p/{state.player_stones}s | "
                          f"Computer: {state.computer_score}p/{state.computer_stones}s\n"
                          f"Value: {state.value if state.value is not None else 'N/A'}")

            pos[node_label] = (x, -y * 2)  # Paplašinām vertikālo atstarpi

            # Nosakām mezgla krāsu atkarībā no heiristiskās vērtības
            if state.value is not None:
                # Pozitīvas vērtības (labvēlīgas datoram) = zaļas, negatīvas (labvēlīgas cilvēkam) = sarkanas
                if state.value > 0:
                    # Zaļās krāsas intensitāte atkarīga no vērtības (0-30+)
                    intensity = min(abs(state.value) / 30.0, 1.0)
                    color = (1 - intensity, 1, 1 - intensity)  # Zaļa (RGB)
                elif state.value < 0:
                    # Sarkanās krāsas intensitāte atkarīga no vērtības (0-30+)
                    intensity = min(abs(state.value) / 30.0, 1.0)
                    color = (1, 1 - intensity, 1 - intensity)  # Sarkana (RGB)
                else:
                    color = 'lightblue'  # Neitrāla vērtība
            else:
                color = 'lightblue'  # Nav vērtības

            graph.add_node(node_label, color=color)

            if parent:
                graph.add_edge(parent, node_label)

            num_children = len(state.children)
            step = width / max(num_children, 1)
            next_x = x - (width / 2) + (step / 2)

            for i, child in enumerate(state.children):
                add_edges(child, node_label, level + 1,
                          next_x + i * step, y + 1, width / 1.5)

        add_edges(root, x=0, y=0)

        plt.figure(figsize=(18, 14))  # Palielinām attēla izmēru
        plt.title(title)

        # Iegūstam mezglu krāsas
        node_colors = [graph.nodes[node].get(
            'color', 'lightblue') for node in graph.nodes()]

        nx.draw(graph, pos, with_labels=True, node_size=3500,
                node_color=node_colors, font_size=8, edge_color='gray')
        plt.tight_layout()
        plt.show()

    def show_game_over(self):
        """Parāda spēles beigu ekrānu"""
        # Aprēķinam rezultātu
        result = self.game_state.calculate_final_score()

        # Informācija par spēles beigām
        self.canvas.create_text(
            187, 300, text="SPĒLE BEIGUSIES", fill="yellow", font=("Arial", 20, "bold"))

        # Galīgie punkti
        final_player_score = self.game_state.player_score + self.game_state.player_stones
        final_computer_score = self.game_state.computer_score + self.game_state.computer_stones

        self.canvas.create_text(187, 340, text=f"Cilvēka gala punkti: {final_player_score}",
                                fill="white", font=("Arial", 14))
        self.canvas.create_text(187, 370, text=f"Datora gala punkti: {final_computer_score}",
                                fill="white", font=("Arial", 14))

        # Uzvarētājs
        self.canvas.create_text(187, 410, text=result,
                                fill="cyan", font=("Arial", 18, "bold"))
        
        # Parādām algoritma metrikas
        self.canvas.create_text(
            187, 450,
            text=f"Kopējais mezglu skaits: {self.total_nodes}",
            fill="white", font=("Arial", 12)
        )
        self.canvas.create_text(
            187, 480,
            text=f"Kopējais laiks: {self.total_time:.4f} s",
            fill="white", font=("Arial", 12)
        )

        # Poga jaunai spēlei
        new_game_btn = tk.Button(self.root, text="Jauna spēle", command=self.new_game,
                                 bg="green", fg="white", font=("Arial", 14))
        self.canvas.create_window(187, 520, window=new_game_btn)

    def new_game(self):
        """Atgriežas uz sākuma ekrānu, lai sāktu jaunu spēli"""
        self.total_nodes = 0
        self.total_time = 0.0
        self.clrscr()
        self.create_ctrl()

    def run(self):
        """Palaiž lietotāja interfeisu"""
        self.root.mainloop()


if __name__ == "__main__":
    game = GameUI()
    game.run()
