import tkinter as tk
import datetime as dt
from tkinter import messagebox
import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("themes/console.json")


# ---------- Configuración inicial ----------
WORK_MIN = 25
BREAK_MIN = 5
DEGRADADO = ("#ff6a00", "#ffcc00")  # naranja → amarillo

class Pomodoro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry("280x150")
        self.resizable(False, False)

        # Siempre sobre otras ventanas
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))  # evita que sea molesto

        self._create_gradient(DEGRADADO)
        self._create_widgets()
        self._reset()

    # --------- Degradado de fondo ----------
    def _create_gradient(self, colors):
        w, h = 280, 150
        canvas = tk.Canvas(self, width=w, height=h, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        r1, g1, b1 = self.winfo_rgb(colors[0])
        r2, g2, b2 = self.winfo_rgb(colors[1])
        steps = h
        for i in range(steps):
            r = int(r1 + (r2 - r1) * i / steps) >> 8
            g = int(g1 + (g2 - g1) * i / steps) >> 8
            b = int(b1 + (b2 - b1) * i / steps) >> 8
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, w, i, fill=color)
        canvas.lower("all")  # fondo

    # --------- Widgets ----------
    def _create_widgets(self):
        self.timer_var = tk.StringVar(value="25:00")
    
        # Crear un frame transparente para el texto
        text_frame = tk.Frame(self, bg="#ff8800")  # Color intermedio del degradado
        text_frame.place(relx=0.5, rely=0.35, anchor="center")
        
        lbl = tk.Label(text_frame, textvariable=self.timer_var, 
                    font=("Consolas", 36), fg="white", bg="#ff8800")
        lbl.pack()

        btn_start = tk.Button(self, text="Iniciar", command=self._start)
        btn_reset = tk.Button(self, text="Reset", command=self._reset)
        btn_up = tk.Button(self, text="+", width=2, command=lambda: self._adjust(60))
        btn_down = tk.Button(self, text="−", width=2, command=lambda: self._adjust(-60))

        btn_start.place(relx=0.25, rely=0.75, anchor="center")
        btn_reset.place(relx=0.75, rely=0.75, anchor="center")
        btn_up.place(relx=0.85, rely=0.35, anchor="w")
        btn_down.place(relx=0.85, rely=0.55, anchor="w")

    # --------- Lógica Pomodoro ----------
    def _adjust(self, seconds):
        self.remaining += seconds
        self.remaining = max(0, self.remaining)
        self._update_label()

    def _start(self):
        self.running = True
        self._countdown()

    def _reset(self):
        self.running = False
        self.remaining = WORK_MIN * 60
        self._update_label()

    def _countdown(self):
        if not self.running:
            return
        if self.remaining <= 0:
            self.running = False
            messagebox.showinfo("Pomodoro", "¡Tiempo terminado!")
            self.remaining = BREAK_MIN * 60
            self._update_label()
            return
        self.remaining -= 1
        self._update_label()
        self.after(1000, self._countdown)

    def _update_label(self):
        mins, secs = divmod(self.remaining, 60)
        self.timer_var.set(f"{mins:02}:{secs:02}")

if __name__ == "__main__":
    Pomodoro().mainloop()
