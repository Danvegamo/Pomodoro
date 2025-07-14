import datetime as dt
import customtkinter as ctk
from PIL import Image
import tkinter.font as tkFont

ctk.set_appearance_mode("dark")
# Si no tienes el archivo themes/console.json, usa el tema oscuro por defecto
# ctk.set_default_color_theme("themes/console.json")

class TitleBar(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, height=28, corner_radius=0, fg_color="#000000", *args, **kwargs)
        self.pack(fill="x")

        # Título de la aplicación
        self.label = ctk.CTkLabel(self, text="🍅 Pomodoro Retro", 
                                 text_color="#00ff00", 
                                 font=ctk.CTkFont(family="Consolas", size=12))
        self.label.pack(side="left", padx=8)

        # Botón de cerrar
        close = ctk.CTkButton(self, text="✕", width=28, height=28, 
                             fg_color="#003200", hover_color="#ff0000",
                             text_color="#00ff00", corner_radius=0,
                             command=master.destroy)
        close.pack(side="right")

        # Hacer la ventana arrastrable
        self.bind("<B1-Motion>", self._move)
        self.label.bind("<B1-Motion>", self._move)
        self.bind("<Button-1>", self._click)
        self.label.bind("<Button-1>", self._click)

    def _click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def _move(self, event):
        x = self.master.winfo_x() + event.x - self.start_x
        y = self.master.winfo_y() + event.y - self.start_y
        self.master.geometry(f"+{x}+{y}")

class SettingsPanel(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Configuración")
        self.geometry("300x220")
        self.configure(fg_color="#000000")
        self.grab_set()  # ventana modal
        
        # Ejemplo de configuración
        ctk.CTkLabel(self, text="Configuraciones", 
                    text_color="#00ff00",
                    font=ctk.CTkFont(family="Consolas", size=16, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(self, text="Tiempo de trabajo (min):", 
                    text_color="#00ff00").pack(pady=5)
        
        self.work_entry = ctk.CTkEntry(self, fg_color="#001a00", 
                                      text_color="#00ff00", 
                                      border_color="#004d00")
        self.work_entry.pack(pady=5)
        self.work_entry.insert(0, "25")
        
        ctk.CTkButton(self, text="Guardar", 
                     fg_color="#003200", hover_color="#004d00",
                     text_color="#00ff00",
                     command=self.destroy).pack(pady=10)

class Pomodoro(ctk.CTk):
    WORK_MIN, BREAK_MIN = 25, 5
    
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.configure(fg_color="#000000")
        self.title("Pomodoro Retro")
        
        # Crear barra de título personalizada
        self.overrideredirect(True)
        TitleBar(self)
        
        # Configurar fuente
        try:
            pixel_font = ctk.CTkFont(family="Press Start 2P", size=20)
            small_font = ctk.CTkFont(family="Press Start 2P", size=12)
        except:
            pixel_font = ctk.CTkFont(family="Consolas", size=20, weight="bold")
            small_font = ctk.CTkFont(family="Consolas", size=12)
        
        # Timer display
        self.timer_var = ctk.StringVar(value="25:00")
        self.timer_label = ctk.CTkLabel(self, textvariable=self.timer_var, 
                                       font=pixel_font, text_color="#00ff00")
        self.timer_label.pack(pady=40)
        
        # Botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(button_frame, text="▶ START", 
                                      width=100, height=40,
                                      fg_color="#003200", hover_color="#004d00",
                                      text_color="#00ff00", font=small_font,
                                      corner_radius=4, command=self._start)
        self.start_btn.pack(side="left", padx=10)
        
        self.reset_btn = ctk.CTkButton(button_frame, text="⟲ RESET", 
                                      width=100, height=40,
                                      fg_color="#003200", hover_color="#004d00",
                                      text_color="#00ff00", font=small_font,
                                      corner_radius=4, command=self._reset)
        self.reset_btn.pack(side="left", padx=10)
        
        # Botón de configuración (sin icono por ahora)
        self.config_btn = ctk.CTkButton(self, text="⚙", width=32, height=32,
                                       fg_color="#003200", hover_color="#004d00",
                                       text_color="#00ff00", corner_radius=4,
                                       command=lambda: SettingsPanel(self))
        self.config_btn.place(relx=0.9, rely=0.15)
        
        # Sistema de puntos
        self.points = 0
        self.points_var = ctk.StringVar(value="Puntos: 0")
        self.points_label = ctk.CTkLabel(self, textvariable=self.points_var, 
                                        font=small_font, text_color="#00ff00")
        self.points_label.place(relx=0.02, rely=0.9)
        
        # Variables de control
        self.running = False
        self.remaining = self.WORK_MIN * 60
        self._update_label()
        
        # Mantener siempre encima
        self.attributes("-topmost", True)
    
    def _update_label(self):
        m, s = divmod(self.remaining, 60)
        self.timer_var.set(f"{m:02}:{s:02}")
    
    def _countdown(self):
        if self.running:
            if self.remaining <= 0:
                self.running = False
                self.points += 1
                self.points_var.set(f"Puntos: {self.points}")
                self.remaining = self.BREAK_MIN * 60
                self._update_label()
                # Aquí podrías agregar una notificación
                print("¡Tiempo terminado!")
            else:
                self.remaining -= 1
                self._update_label()
                self.after(1000, self._countdown)
    
    def _start(self):
        if not self.running:
            self.running = True
            self.start_btn.configure(text="⏸ PAUSE")
            self._countdown()
        else:
            self.running = False
            self.start_btn.configure(text="▶ START")
    
    def _reset(self):
        self.running = False
        self.remaining = self.WORK_MIN * 60
        self.start_btn.configure(text="▶ START")
        self._update_label()

if __name__ == "__main__":
    Pomodoro().mainloop()
