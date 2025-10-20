from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
import random
import os

from scores import write_score


class GameWindow(Toplevel):
    """Memorama game window with click validation, matching logic and basic scoring."""

    def __init__(self, master, grid_size: int = 4, theme_dir: str = "ImagenesPython", player_name: str | None = None):
        super().__init__(master)
        self.title("Memorama - Programación")
        self.geometry("800x800")
        self.minsize(600, 600)
        self.grid_size = grid_size
        self.theme_dir = theme_dir
        self.player_name = player_name or self._prompt_name()
        self.difficulty = self._difficulty_from_grid(grid_size)
        self.configure(bg="#0f172a")  # slate-900

        # UI: header with status and reset
        header = Frame(self, bg="#0f172a")
        header.pack(side=TOP, fill=X, padx=16, pady=12)

        self.status_var = StringVar(value=f"Jugador: {self.player_name} | Dificultad: {self.difficulty} | Intentos: 0 | Aciertos: 0")
        lbl = Label(header, textvariable=self.status_var, fg="#e2e8f0", bg="#0f172a", font=("Lato", 14, "bold"))
        lbl.pack(side=LEFT)

        self.reset_btn = Button(header, text="Reiniciar", command=self.reset_game, bg="#22c55e", fg="white", activebackground="#16a34a", relief=GROOVE)
        self.reset_btn.pack(side=RIGHT)

        # Game board frame
        self.board = Frame(self, bg="#0f172a")
        self.board.pack(expand=True, fill=BOTH, padx=16, pady=16)

        # Load images
        self.front_img = None  # back of card (common)
        self.card_images = []  # per pair
        self.buttons = []
        self.card_values = []  # pair identifiers
        self.revealed_indices = []
        self.lock_input = False
        self.attempts = 0
        self.matches = 0

        self._load_images()
        self._build_grid()
        self.bind("<Configure>", self._on_resize)
        # Music and close protocol
        self._mixer = None
        self._music_on = False
        self._init_music()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _prompt_name(self) -> str:
        name = simpledialog.askstring("Jugador", "Ingresa tu nombre para guardar tu puntaje:", parent=self)
        if not name:
            name = "Invitado"
        return name.strip() or "Invitado"

    def _difficulty_from_grid(self, gs: int) -> str:
        return "facil" if gs == 4 else "medio" if gs == 5 else "dificil"

    def _asset_paths(self):
        # choose a default back and N unique faces from theme dir
        files = [f for f in os.listdir(self.theme_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        files.sort()
        if not files:
            raise RuntimeError("No se encontraron imágenes en la carpeta de tema")
        back = files[0]
        # need grid_size*grid_size/2 unique faces
        need = (self.grid_size * self.grid_size) // 2
        faces = files[1:1+need]
        if len(faces) < need:
            # fallback by repeating
            faces = (faces * ((need // max(1, len(faces))) + 1))[:need]
        return os.path.join(self.theme_dir, back), [os.path.join(self.theme_dir, f) for f in faces]

    def _load_images(self):
        back_path, face_paths = self._asset_paths()
        # placeholders; actual resize happens on draw/resize
        self.front_src = Image.open(back_path)
        self.face_srcs = [Image.open(p) for p in face_paths]

        # pair assignment
        ids = list(range(len(self.face_srcs)))
        pairs = ids * 2
        random.shuffle(pairs)
        self.card_values = pairs

    def _build_grid(self):
        # clear previous
        for w in self.board.winfo_children():
            w.destroy()
        self.buttons.clear()
        gs = self.grid_size
        for r in range(gs):
            self.board.rowconfigure(r, weight=1)
            for c in range(gs):
                self.board.columnconfigure(c, weight=1)
                idx = r * gs + c
                btn = Button(self.board, relief=RAISED, bd=2, bg="#1f2937", activebackground="#374151")
                btn.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)
                btn.configure(command=lambda i=idx: self.on_card_click(i))
                self.buttons.append(btn)
        self._redraw_images()

    def _card_size(self):
        # estimate cell size based on board size
        bw = max(self.board.winfo_width(), 200)
        bh = max(self.board.winfo_height(), 200)
        gs = self.grid_size
        cw = bw // gs - 20
        ch = bh // gs - 20
        side = max(32, min(cw, ch))
        return side, side

    def _redraw_images(self):
        w, h = self._card_size()
        self.front_img = ImageTk.PhotoImage(self.front_src.resize((w, h)))
        self.card_images = [ImageTk.PhotoImage(img.resize((w, h))) for img in self.face_srcs]
        for i, btn in enumerate(self.buttons):
            # keep revealed pairs face-up; show current first selection; others back
            if i in self.revealed_indices:
                face_id = self.card_values[i]
                btn.config(image=self.card_images[face_id])
                btn.image = self.card_images[face_id]
            elif getattr(self, "first_index", None) == i and not self.lock_input:
                face_id = self.card_values[i]
                btn.config(image=self.card_images[face_id])
                btn.image = self.card_images[face_id]
            else:
                btn.config(image=self.front_img)
                btn.image = self.front_img

    def _on_resize(self, _event):
        self.after(50, self._redraw_images)

    def _init_music(self):
        """Start background music if pygame is available and the file exists."""
        try:
            # Import locally to avoid hard dependency if not installed
            import pygame
            from pygame import mixer
            if not pygame.get_init():
                pygame.init()
            if not mixer.get_init():
                mixer.init()
            base_dir = os.path.dirname(os.path.abspath(__file__))
            music_path = os.path.join(base_dir, "musica.mp3")
            if os.path.exists(music_path):
                mixer.music.load(music_path)
                mixer.music.play(-1)  # loop
                self._mixer = mixer
                self._music_on = True
        except Exception:
            # Silently ignore if pygame or device not available
            self._mixer = None
            self._music_on = False

    def _stop_music(self):
        try:
            if self._mixer and self._music_on:
                self._mixer.music.stop()
                self._mixer.quit()
        except Exception:
            pass
        finally:
            self._mixer = None
            self._music_on = False

    def on_card_click(self, index: int):
        if self.lock_input:
            return
        if index < 0 or index >= len(self.buttons):
            return
        if index in self.revealed_indices:
            # already matched; ignore
            return

        # If the card is temporarily face-up in current attempt, ignore
        # Find if index is already the first selection
        if getattr(self, "first_index", None) == index:
            return

        # reveal card
        face_id = self.card_values[index]
        self.buttons[index].config(image=self.card_images[face_id])
        self.buttons[index].image = self.card_images[face_id]

        if not hasattr(self, "first_index") or self.first_index is None:
            self.first_index = index
            self._update_status()
            return

        # second click
        second_index = index
        first_id = self.card_values[self.first_index]
        second_id = self.card_values[second_index]
        self.attempts += 1
        if first_id == second_id and self.first_index != second_index:
            # match
            self.revealed_indices.extend([self.first_index, second_index])
            self.matches += 1
            self.first_index = None
            self._update_status()
            if self.matches == len(self.card_values) // 2:
                self._win()
        else:
            # no match -> flip back after short delay
            fi, si = self.first_index, second_index
            self.first_index = None
            self.lock_input = True
            self.after(700, lambda: self._flip_back(fi, si))
            self._update_status()

    def _flip_back(self, i: int, j: int):
        if i not in self.revealed_indices:
            self.buttons[i].config(image=self.front_img)
            self.buttons[i].image = self.front_img
        if j not in self.revealed_indices:
            self.buttons[j].config(image=self.front_img)
            self.buttons[j].image = self.front_img
        self.lock_input = False

    def _score(self) -> int:
        total_pairs = len(self.card_values) // 2
        # simple scoring: start from 1000 and subtract attempts beyond optimal
        penalty = max(0, self.attempts - total_pairs)
        return max(0, 1000 - penalty * 20)

    def _update_status(self):
        self.status_var.set(
            f"Jugador: {self.player_name} | Dificultad: {self.difficulty} | Intentos: {self.attempts} | Aciertos: {self.matches} | Puntaje: {self._score()}"
        )

    def _win(self):
        score = self._score()
        write_score(self.player_name, score, difficulty=self.difficulty)
        # Custom modal popup with 'Salir' button
        popup = Toplevel(self)
        popup.title("¡Ganaste!")
        popup.configure(bg="#0f172a")
        popup.transient(self)
        popup.grab_set()

        msg = Label(popup, text=f"¡Completaste el memorama!\nPuntaje: {score}", fg="#e2e8f0", bg="#0f172a", font=("Lato", 16, "bold"))
        msg.pack(padx=24, pady=(24, 12))

        btn = Button(popup, text="Salir", command=lambda: self._close_after_popup(popup), bg="#ef4444", fg="white", activebackground="#dc2626")
        btn.pack(pady=(0, 24), ipadx=16, ipady=6)

        # Center popup over game window
        self.update_idletasks()
        pw, ph = 360, 160
        try:
            gx = self.winfo_rootx()
            gy = self.winfo_rooty()
            gw = self.winfo_width()
            gh = self.winfo_height()
            x = gx + (gw - pw) // 2
            y = gy + (gh - ph) // 2
            popup.geometry(f"{pw}x{ph}+{x}+{y}")
        except Exception:
            popup.geometry(f"{pw}x{ph}")

        popup.bind("<Escape>", lambda _e: self._close_after_popup(popup))

    def _on_close(self):
        self._stop_music()
        self.destroy()

    def _close_after_popup(self, popup: Toplevel):
        try:
            popup.grab_release()
            popup.destroy()
        except Exception:
            pass
        self._on_close()

    def reset_game(self):
        # reshuffle
        ids = list(range(len(self.face_srcs)))
        pairs = ids * 2
        random.shuffle(pairs)
        self.card_values = pairs
        self.revealed_indices.clear()
        self.first_index = None
        self.lock_input = False
        self.attempts = 0
        self.matches = 0
        self._redraw_images()
        self._update_status()


# Allow running this file directly for quick test
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # hide root; game is a Toplevel
    GameWindow(root, grid_size=4)
    root.mainloop()
