from tkinter import *
from tkinter import ttk

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 770

FIELD_WIDTH = 400
FIELD_HEIGHT = 553

PLAYER_WIDTH = 100
PLAYER_HEIGHT = 106

class FootballField:
    def __init__(self, root):
        self.root = root
        self.root.title("Alineación táctica")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.images = []
        self.players = []

        # Calcular centro
        self.offset_x = (WINDOW_WIDTH - FIELD_WIDTH) // 2
        self.offset_y = (WINDOW_HEIGHT - FIELD_HEIGHT) // 2

        # Fondo (cancha centrada)
        self.bg_image = PhotoImage(file="assets/cancha.png")
        self.images.append(self.bg_image)

        self.background = Label(root, image=self.bg_image)
        self.background.place(x=self.offset_x, y=self.offset_y)

        # Posiciones RELATIVAS a la cancha
        self.positions = [
            (150, 480),  # Arquero
            (50, 380), (120, 380), (200, 380), (270, 380),
            (80, 260), (160, 260), (240, 260),
            (80, 120), (160, 120), (240, 120)
        ]

        self.create_players()

        self.drag_data = {"widget": None, "x": 0, "y": 0}

    def create_players(self):
        for i in range(11):
            img = PhotoImage(file=f"assets/jugador{i+1}.png")
            self.images.append(img)

            label = Label(self.root, image=img, bd=0)

            # Ajustar posición sumando offset
            x, y = self.positions[i]
            label.place(
                x=x + self.offset_x,
                y=y + self.offset_y,
                width=PLAYER_WIDTH,
                height=PLAYER_HEIGHT
            )

            label.bind("<Button-1>", self.on_start_drag)
            label.bind("<B1-Motion>", self.on_drag)
            label.bind("<ButtonRelease-1>", self.on_drop)

            self.players.append(label)

    def on_start_drag(self, event):
        self.drag_data["widget"] = event.widget
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag(self, event):
        widget = self.drag_data["widget"]
        if widget:
            x = widget.winfo_x() + (event.x - self.drag_data["x"])
            y = widget.winfo_y() + (event.y - self.drag_data["y"])
            widget.place(x=x, y=y)

    def on_drop(self, event):
        widget = self.drag_data["widget"]
        if not widget:
            return

        for other in self.players:
            if other == widget:
                continue

            if self.is_overlap(widget, other):
                x1, y1 = widget.winfo_x(), widget.winfo_y()
                x2, y2 = other.winfo_x(), other.winfo_y()

                widget.place(x=x2, y=y2)
                other.place(x=x1, y=y1)
                break

        self.drag_data["widget"] = None

    def is_overlap(self, w1, w2):
        x1, y1 = w1.winfo_x(), w1.winfo_y()
        x2, y2 = w2.winfo_x(), w2.winfo_y()

        return (
            abs(x1 - x2) < PLAYER_WIDTH // 2 and
            abs(y1 - y2) < PLAYER_HEIGHT // 2
        )


if __name__ == "__main__":
    root = Tk()
    app = FootballField(root)
    root.mainloop()