import tkinter as tk
from PIL import ImageTk, Image
from tree import GameState, generate_game_tree

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Akmentini")
        self.root.geometry("375x667")
        self.create_bg()
        self.create_ctrl()
        self.game_state = None  # Sākotnēji spēles stāvoklis nav iestatīts

    def clrscr(self):
        for widget in self.canvas.find_all():
            if widget != 1:  # 1 is typically the background image ID
                self.canvas.delete(widget)
        
    def create_bg(self):
        bg_image = Image.open("bin/background.png").resize((375, 667))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas = tk.Canvas(self.root, width=375, height=667)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def create_ctrl(self):
        title_image = Image.open("bin/Akmentiņi.png").resize((187, 50))
        self.title_photo = ImageTk.PhotoImage(title_image)
        self.canvas.create_image(187, 80, image=self.title_photo, anchor="center")

        self.count = tk.IntVar(value=50)

        left_img = Image.open("bin/left.png").resize((50, 50))
        self.left_photo = ImageTk.PhotoImage(left_img)
        right_img = Image.open("bin/right.png").resize((50, 50))
        self.right_photo = ImageTk.PhotoImage(right_img)

        left_btn = tk.Button(self.root, image=self.left_photo, borderwidth=0, command=self.ctr_decrease, bg="black")
        right_btn = tk.Button(self.root, image=self.right_photo, borderwidth=0, command=self.ctr_increase, bg="black")

        self.canvas.create_window(150, 300, window=left_btn)
        self.canvas.create_window(225, 300, window=right_btn)

        label = tk.Label(self.root, textvariable=self.count, font=("Arial", 40, "bold"), bg="black", fg="white", width=5)
        self.canvas.create_window(187, 240, window=label)

        start_img = Image.open("bin/start.png").resize((150, 50))
        self.start_photo = ImageTk.PhotoImage(start_img)
        start_btn = tk.Button(self.root, image=self.start_photo, borderwidth=0, command=self.start_game, bg="black")
        exit_img = Image.open("bin/exit.png").resize((150, 50))
        self.exit_photo = ImageTk.PhotoImage(exit_img)
        exit_btn = tk.Button(self.root, image=self.exit_photo, borderwidth=0, command=self.exit_game, bg="black")

        self.canvas.create_window(187, 400, window=start_btn)
        self.canvas.create_window(187, 480, window=exit_btn)

    def ctr_increase(self):
        if self.count.get() < 70:
            self.count.set(self.count.get() + 1)

    def ctr_decrease(self):
        if self.count.get() > 50:
            self.count.set(self.count.get() - 1)

    def start_game(self):
        self.clrscr()
        # self.game_state = GameState(self.count.get(), True, 0, 0)
        # self.game_state = generate_game_tree(self.game_state, max_depth=5)
        self.player_sel()

    def exit_game(self):
        self.root.destroy()

    def player_sel(self):
        human_image = Image.open("bin/human.png").resize((75, 75))
        self.human_photo = ImageTk.PhotoImage(human_image)
        computer_image = Image.open("bin/computer.png").resize((75, 75))
        self.computer_photo = ImageTk.PhotoImage(computer_image)

        human_btn = tk.Button(
            self.root, 
            image=self.human_photo,
            borderwidth=0,
            command=self.start_human,
            bg="black"
        )
        
        computer_btn = tk.Button(
            self.root,
            image=self.computer_photo,
            borderwidth=0, 
            command=self.start_computer,
            bg="black"
        )

        self.canvas.create_window(187, 300, window=human_btn)
        self.canvas.create_window(187, 400, window=computer_btn)

    def start_computer(self):
        self.clrscr()

    def start_human(self):
        self.clrscr()

    def run(self):
        self.root.mainloop()

def main():
    game = UI()
    game.run()

main()