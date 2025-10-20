from tkinter import *
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
from tkinter import font

from ventana import GameWindow
from scores import read_scores


class ScoresWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Puntajes máximos")
        self.geometry("500x400")
        self.configure(bg="#0f172a")

        title = Label(self, text="Puntajes máximos", fg="#e2e8f0", bg="#0f172a", font=("Lato", 18, "bold"))
        title.pack(pady=12)

        cols = ("Jugador", "Puntaje", "Dificultad")
        tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c in cols:
            tree.heading(c, text=c)
            width = 160 if c == "Dificultad" else 160
            tree.column(c, anchor=CENTER, width=width)
        tree.pack(expand=True, fill=BOTH, padx=12, pady=12)

        # populate
        scores = read_scores()
        for entry in scores:
            tree.insert("", END, values=(entry.get("name"), entry.get("score"), entry.get("difficulty")))


def launch_menu():
    app = Tk()
    app.title('Menu Memorama')
    w, h = 800, 800
    app.geometry(f"{w}x{h}")

    frame = Frame(app, bg="#0f172a")

    # fondo opcional
    try:
        image = Image.open('./photos/nubes.jpg').resize((w, h))
        bg_image = ImageTk.PhotoImage(image)
        bg_label = Label(frame, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception:
        pass

    for i in range(3):
        frame.columnconfigure(i, weight=1)

    frame.rowconfigure(0, weight=3)
    for r in (1, 2, 3):
        frame.rowconfigure(r, weight=1)

    frame.pack(expand=True, fill=BOTH)

    bipady = 10
    bipadx = 100

    label = Label(frame, text="Compurama!", font=("Lato", 40), fg="#e2e8f0", bg="#0f172a")
    label.grid(column=1, row=0, ipady=25, pady=(0, 35), sticky='sew')

    # store player name on the root to ask only once per session
    app.player_name = None
    # difficulty selection
    diff_var = StringVar(value="dificil")  # default 6x6

    def _grid_for_diff(d: str) -> int:
        d = (d or "").lower()
        return 4 if d == "facil" else 5 if d == "medio" else 6

    def start_game():
        if not app.player_name:
            name = simpledialog.askstring("Jugador", "Ingresa tu nombre para guardar tu puntaje:", parent=app)
            app.player_name = (name or "Invitado").strip() or "Invitado"
        gs = _grid_for_diff(diff_var.get())
        GameWindow(app, grid_size=gs, player_name=app.player_name)

    def open_scores():
        ScoresWindow(app)

    # Difficulty radio buttons
    diff_frame = Frame(frame, bg="#0f172a")
    diff_frame.grid(column=1, row=1, sticky='nswe')
    Label(diff_frame, text="Dificultad:", bg="#0f172a", fg="#e2e8f0", font=("Lato", 12, "bold")).pack(pady=(0,6))
    rb1 = ttk.Radiobutton(diff_frame, text="Fácil (4x4)", value="facil", variable=diff_var)
    rb2 = ttk.Radiobutton(diff_frame, text="Medio (5x5)", value="medio", variable=diff_var)
    rb3 = ttk.Radiobutton(diff_frame, text="Difícil (6x6)", value="dificil", variable=diff_var)
    for rb in (rb1, rb2, rb3):
        rb.pack(anchor=CENTER, pady=2)

    empezar = Button(frame, text="Empezar", command=start_game, bg="#0f172a", fg="white", activebackground="#16a34a")
    empezar.grid(column=1, row=2, ipady=bipady, ipadx=bipadx, sticky='nswe', pady=20)

    puntajes = Button(frame, text="Puntajes máximos", command=open_scores, bg="#0f172a", fg="white", activebackground="#2563eb")
    puntajes.grid(column=1, row=3, ipady=bipady, ipadx=bipadx, sticky='nswe', pady=20)

    salir = Button(frame, text="Salir", command=app.destroy, bg="#0f172a", fg="white", activebackground="#dc2626")
    salir.grid(column=1, row=4, ipady=bipady, ipadx=bipadx, sticky='nswe', pady=20)

    fuente = font.Font(family='Lato', size=12)
    for b in (empezar, puntajes, salir):
        b.config(font=fuente)

    app.mainloop()


if __name__ == "__main__":
    launch_menu()

