import datetime as dt
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.font as tkFont
import json
import os
import threading
import time
import winsound
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTk
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import webbrowser

ctk.set_appearance_mode("dark")

class DataManager:
    """Gestor de persistencia de datos"""
    
    def __init__(self):
        self.data_dir = "pomodoro_data"
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Crear directorio de datos si no existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_settings(self):
        """Cargar configuración desde JSON"""
        settings_file = os.path.join(self.data_dir, "settings.json")
        default_settings = {
            "work_time": 25,
            "break_time": 5,
            "theme": "Terminal",
            "sound_enabled": True,
            "sound_volume": 50
        }
        
        try:
            with open(settings_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_settings(default_settings)
            return default_settings
    
    def save_settings(self, settings):
        """Guardar configuración en JSON"""
        settings_file = os.path.join(self.data_dir, "settings.json")
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
    
    def load_user_data(self):
        """Cargar datos del usuario"""
        user_file = os.path.join(self.data_dir, "user_data.json")
        default_data = {
            "total_points": 0,
            "level": 1,
            "experience": 0,
            "completed_sessions": 0,
            "total_focus_time": 0,
            "achievements": [],
            "daily_stats": {}
        }
        
        try:
            with open(user_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_user_data(default_data)
            return default_data
    
    def save_user_data(self, user_data):
        """Guardar datos del usuario"""
        user_file = os.path.join(self.data_dir, "user_data.json")
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
    
    def log_session(self, session_type, duration, completed):
        """Registrar sesión completada"""
        today = dt.datetime.now().strftime("%Y-%m-%d")
        sessions_file = os.path.join(self.data_dir, "sessions.json")
        
        session_data = {
            "date": today,
            "time": dt.datetime.now().strftime("%H:%M:%S"),
            "type": session_type,  # "work" or "break"
            "duration": duration,
            "completed": completed
        }
        
        try:
            with open(sessions_file, 'r') as f:
                sessions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            sessions = []
        
        sessions.append(session_data)
        
        with open(sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)

class SoundManager:
    """Gestor de sonidos y notificaciones"""
    
    def __init__(self):
        self.sounds_enabled = True
        self.volume = 50
    
    def play_completion_sound(self):
        """Reproducir sonido de completación"""
        if self.sounds_enabled:
            try:
                # Sonido de Windows predeterminado
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            except:
                # Sonido alternativo si falla
                print("\a")  # Bell character
    
    def play_start_sound(self):
        """Sonido al iniciar sesión"""
        if self.sounds_enabled:
            try:
                winsound.Beep(800, 200)
            except:
                print("\a")
    
    def play_pause_sound(self):
        """Sonido al pausar"""
        if self.sounds_enabled:
            try:
                winsound.Beep(400, 300)
            except:
                print("\a")

class AchievementSystem:
    """Sistema de logros y niveles"""
    
    ACHIEVEMENTS = {
        "first_session": {"name": "Primer Paso", "desc": "Completa tu primera sesión", "icon": "🎯"},
        "streak_5": {"name": "Racha Iniciada", "desc": "5 sesiones seguidas", "icon": "🔥"},
        "streak_10": {"name": "En Llamas", "desc": "10 sesiones seguidas", "icon": "💥"},
        "total_50": {"name": "Veterano", "desc": "50 sesiones totales", "icon": "⭐"},
        "total_100": {"name": "Maestro del Tiempo", "desc": "100 sesiones totales", "icon": "👑"},
        "perfect_day": {"name": "Día Perfecto", "desc": "8 sesiones en un día", "icon": "✨"},
        "night_owl": {"name": "Búho Nocturno", "desc": "Sesión después de las 10 PM", "icon": "🦉"},
        "early_bird": {"name": "Madrugador", "desc": "Sesión antes de las 6 AM", "icon": "🐦"}
    }
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.user_data = data_manager.load_user_data()
    
    def check_achievements(self, session_data):
        """Verificar y otorgar logros"""
        new_achievements = []
        
        # Primer sesión
        if self.user_data["completed_sessions"] == 1 and "first_session" not in self.user_data["achievements"]:
            new_achievements.append("first_session")
        
        # Total de sesiones
        total = self.user_data["completed_sessions"]
        if total >= 50 and "total_50" not in self.user_data["achievements"]:
            new_achievements.append("total_50")
        if total >= 100 and "total_100" not in self.user_data["achievements"]:
            new_achievements.append("total_100")
        
        # Día perfecto (8 sesiones en un día)
        today = dt.datetime.now().strftime("%Y-%m-%d")
        if today in self.user_data["daily_stats"]:
            if self.user_data["daily_stats"][today] >= 8 and "perfect_day" not in self.user_data["achievements"]:
                new_achievements.append("perfect_day")
        
        # Horarios especiales
        current_hour = dt.datetime.now().hour
        if current_hour >= 22 and "night_owl" not in self.user_data["achievements"]:
            new_achievements.append("night_owl")
        if current_hour <= 6 and "early_bird" not in self.user_data["achievements"]:
            new_achievements.append("early_bird")
        
        # Agregar nuevos logros
        for achievement in new_achievements:
            self.user_data["achievements"].append(achievement)
        
        return new_achievements
    
    def calculate_level(self):
        """Calcular nivel basado en experiencia"""
        exp = self.user_data["experience"]
        level = 1 + (exp // 100)  # Cada 100 puntos = 1 nivel
        return min(level, 50)  # Máximo nivel 50
    
    def add_experience(self, points):
        """Agregar experiencia"""
        self.user_data["experience"] += points
        self.user_data["level"] = self.calculate_level()

class StatsPanel(ctk.CTkToplevel):
    """Panel de estadísticas con gráficas"""
    
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        self.title("📊 Estadísticas de Productividad")
        self.geometry("800x600")
        self.configure(fg_color=master.current_theme["bg"])
        
        self.create_stats_widgets()
    
    def create_stats_widgets(self):
        """Crear widgets de estadísticas"""
        theme = self.master.current_theme
        
        # Título
        title = ctk.CTkLabel(self, text="📊 Estadísticas de Productividad",
                           font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                           text_color=theme["fg"])
        title.pack(pady=10)
        
        # Notebook para pestañas
        notebook = ctk.CTkTabview(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Pestaña resumen
        summary_tab = notebook.add("Resumen")
        self.create_summary_tab(summary_tab, theme)
        
        # Pestaña gráficas
        charts_tab = notebook.add("Gráficas")
        self.create_charts_tab(charts_tab, theme)
        
        # Pestaña logros
        achievements_tab = notebook.add("Logros")
        self.create_achievements_tab(achievements_tab, theme)
    
    def create_summary_tab(self, tab, theme):
        """Crear pestaña de resumen"""
        user_data = self.data_manager.load_user_data()
        
        # Estadísticas principales
        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        stats = [
            ("Nivel", f"{user_data['level']}"),
            ("Puntos Totales", f"{user_data['total_points']}"),
            ("Sesiones Completadas", f"{user_data['completed_sessions']}"),
            ("Tiempo de Enfoque", f"{user_data['total_focus_time']//60}h {user_data['total_focus_time']%60}m"),
            ("Logros Desbloqueados", f"{len(user_data['achievements'])}")
        ]
        
        for i, (label, value) in enumerate(stats):
            row = ctk.CTkFrame(stats_frame, fg_color=theme["btn_bg"])
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(row, text=label, text_color=theme["fg"]).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=value, text_color=theme["fg"], 
                        font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10)
    
    def create_charts_tab(self, tab, theme):
        """Crear pestaña de gráficas"""
        try:
            # Cargar datos de sesiones
            sessions_file = os.path.join(self.data_manager.data_dir, "sessions.json")
            with open(sessions_file, 'r') as f:
                sessions = json.load(f)
            
            if not sessions:
                ctk.CTkLabel(tab, text="No hay datos suficientes para mostrar gráficas",
                           text_color=theme["fg"]).pack(pady=50)
                return
            
            # Crear gráfica de productividad diaria
            df = pd.DataFrame(sessions)
            daily_stats = df.groupby('date').size()
            
            # Configurar matplotlib para el tema oscuro
            plt.style.use('dark_background')
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            fig.patch.set_facecolor(theme["bg"])
            
            # Gráfica de sesiones por día
            daily_stats.plot(kind='bar', ax=ax1, color=theme["fg"])
            ax1.set_title('Sesiones por Día', color=theme["fg"])
            ax1.set_xlabel('Fecha', color=theme["fg"])
            ax1.set_ylabel('Sesiones', color=theme["fg"])
            
            # Gráfica de distribución por horas
            df['hour'] = pd.to_datetime(df['time']).dt.hour
            hourly_stats = df.groupby('hour').size()
            hourly_stats.plot(kind='line', ax=ax2, color=theme["fg"], marker='o')
            ax2.set_title('Distribución por Horas del Día', color=theme["fg"])
            ax2.set_xlabel('Hora', color=theme["fg"])
            ax2.set_ylabel('Sesiones', color=theme["fg"])
            
            plt.tight_layout()
            
            # Integrar en la ventana
            canvas = FigureCanvasTk(fig, tab)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            ctk.CTkLabel(tab, text=f"Error al generar gráficas: {str(e)}",
                       text_color=theme["fg"]).pack(pady=50)
    
    def create_achievements_tab(self, tab, theme):
        """Crear pestaña de logros"""
        user_data = self.data_manager.load_user_data()
        
        # Scrollable frame para logros
        scrollable = ctk.CTkScrollableFrame(tab)
        scrollable.pack(fill="both", expand=True, padx=20, pady=10)
        
        for key, achievement in AchievementSystem.ACHIEVEMENTS.items():
            unlocked = key in user_data["achievements"]
            
            # Frame para cada logro
            achievement_frame = ctk.CTkFrame(scrollable, 
                                           fg_color=theme["btn_bg"] if unlocked else theme["entry_bg"])
            achievement_frame.pack(fill="x", pady=5)
            
            # Icono y texto
            icon_color = theme["fg"] if unlocked else "#666666"
            text_color = theme["fg"] if unlocked else "#666666"
            
            ctk.CTkLabel(achievement_frame, text=achievement["icon"], 
                        font=ctk.CTkFont(size=24)).pack(side="left", padx=10)
            
            info_frame = ctk.CTkFrame(achievement_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10)
            
            ctk.CTkLabel(info_frame, text=achievement["name"], 
                        text_color=text_color, 
                        font=ctk.CTkFont(weight="bold")).pack(anchor="w")
            ctk.CTkLabel(info_frame, text=achievement["desc"], 
                        text_color=text_color).pack(anchor="w")
            
            if unlocked:
                ctk.CTkLabel(achievement_frame, text="✓ DESBLOQUEADO", 
                           text_color="#00ff00").pack(side="right", padx=10)

class ReportExporter:
    """Exportador de reportes"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def export_pdf_report(self):
        """Exportar reporte en PDF"""
        try:
            user_data = self.data_manager.load_user_data()
            
            # Crear PDF
            filename = f"reporte_pomodoro_{dt.datetime.now().strftime('%Y%m%d')}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            
            # Título
            c.setFont("Helvetica-Bold", 24)
            c.drawString(50, 750, "Reporte de Productividad Pomodoro")
            
            # Estadísticas
            c.setFont("Helvetica", 14)
            y = 700
            stats = [
                f"Nivel: {user_data['level']}",
                f"Puntos Totales: {user_data['total_points']}",
                f"Sesiones Completadas: {user_data['completed_sessions']}",
                f"Tiempo Total de Enfoque: {user_data['total_focus_time']//60}h {user_data['total_focus_time']%60}m",
                f"Logros Desbloqueados: {len(user_data['achievements'])}",
                f"Fecha del Reporte: {dt.datetime.now().strftime('%d/%m/%Y')}"
            ]
            
            for stat in stats:
                c.drawString(50, y, stat)
                y -= 30
            
            # Logros
            y -= 20
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, "Logros Desbloqueados:")
            y -= 20
            
            c.setFont("Helvetica", 12)
            for achievement_key in user_data['achievements']:
                if achievement_key in AchievementSystem.ACHIEVEMENTS:
                    achievement = AchievementSystem.ACHIEVEMENTS[achievement_key]
                    c.drawString(70, y, f"• {achievement['name']}: {achievement['desc']}")
                    y -= 20
            
            c.save()
            return filename
        except Exception as e:
            return None
    
    def export_csv_data(self):
        """Exportar datos en CSV"""
        try:
            sessions_file = os.path.join(self.data_manager.data_dir, "sessions.json")
            with open(sessions_file, 'r') as f:
                sessions = json.load(f)
            
            df = pd.DataFrame(sessions)
            filename = f"datos_pomodoro_{dt.datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(filename, index=False)
            return filename
        except Exception as e:
            return None

# [Resto del código de las clases anteriores: ThemeManager, MiniTimer, SettingsPanel, TitleBar]
class ThemeManager:
    """Gestor de temas estilo Obsidian"""
    
    THEMES = {
        "Terminal": {
            "bg": "#000000", "fg": "#00ff00", "btn_bg": "#003200", 
            "btn_hover": "#004d00", "entry_bg": "#001a00"
        },
        "Matrix": {
            "bg": "#0d1117", "fg": "#58a6ff", "btn_bg": "#1f2937", 
            "btn_hover": "#374151", "entry_bg": "#111827"
        },
        "Cyberpunk": {
            "bg": "#1a0d26", "fg": "#ff00ff", "btn_bg": "#2d1b3d", 
            "btn_hover": "#3d2b4d", "entry_bg": "#0f0515"
        },
        "Retro Amber": {
            "bg": "#1a0f00", "fg": "#ffb000", "btn_bg": "#332200", 
            "btn_hover": "#4d3300", "entry_bg": "#261900"
        }
    }
    
    @classmethod
    def get_theme(cls, name):
        return cls.THEMES.get(name, cls.THEMES["Terminal"])

class Pomodoro(ctk.CTk):
    """Aplicación principal completa"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar managers
        self.data_manager = DataManager()
        self.sound_manager = SoundManager()
        self.achievement_system = AchievementSystem(self.data_manager)
        self.report_exporter = ReportExporter(self.data_manager)
        
        # Cargar configuración
        self.settings = self.data_manager.load_settings()
        self.user_data = self.data_manager.load_user_data()
        
        # Configuración inicial
        self.WORK_MIN = self.settings["work_time"]
        self.BREAK_MIN = self.settings["break_time"]
        self.current_theme_name = self.settings["theme"]
        self.current_theme = ThemeManager.get_theme(self.current_theme_name)
        
        # Variables de control
        self.running = False
        self.remaining = self.WORK_MIN * 60
        self.current_session_type = "work"
        self.session_start_time = None
        self.pause_thread = None
        self.pause_start_time = None
        
        # Configurar ventana
        self.setup_window()
        self.create_widgets()
        self._update_label()
        self.attributes("-topmost", True)
    
    def setup_window(self):
        """Configurar ventana principal"""
        self.geometry("450x350")
        self.configure(fg_color=self.current_theme["bg"])
        self.title("Pomodoro Pro")
        self.overrideredirect(True)
        
        # Crear barra de título
        TitleBar(self)
    
    def create_widgets(self):
        """Crear todos los widgets"""
        theme = self.current_theme
        
        # Fuentes
        try:
            pixel_font = ctk.CTkFont(family="Press Start 2P", size=20)
            small_font = ctk.CTkFont(family="Press Start 2P", size=12)
        except:
            pixel_font = ctk.CTkFont(family="Consolas", size=20, weight="bold")
            small_font = ctk.CTkFont(family="Consolas", size=12)
        
        # Timer display
        self.timer_var = ctk.StringVar(value="25:00")
        self.timer_label = ctk.CTkLabel(self, textvariable=self.timer_var,
                                       font=pixel_font, text_color=theme["fg"])
        self.timer_label.pack(pady=30)
        
        # Indicador de sesión
        self.session_var = ctk.StringVar(value="Trabajo")
        session_label = ctk.CTkLabel(self, textvariable=self.session_var,
                                   font=small_font, text_color=theme["fg"])
        session_label.pack()
        
        # Botones principales
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(button_frame, text="▶ START",
                                      width=100, height=40,
                                      fg_color=theme["btn_bg"],
                                      hover_color=theme["btn_hover"],
                                      text_color=theme["fg"],
                                      font=small_font,
                                      corner_radius=4,
                                      command=self._start)
        self.start_btn.pack(side="left", padx=10)
        
        self.reset_btn = ctk.CTkButton(button_frame, text="⟲ RESET",
                                      width=100, height=40,
                                      fg_color=theme["btn_bg"],
                                      hover_color=theme["btn_hover"],
                                      text_color=theme["fg"],
                                      font=small_font,
                                      corner_radius=4,
                                      command=self._reset)
        self.reset_btn.pack(side="left", padx=10)
        
        # Botones de herramientas
        tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame.pack(pady=10)
        
        # Configuración
        config_btn = ctk.CTkButton(tools_frame, text="⚙", width=50,
                                  fg_color=theme["btn_bg"],
                                  hover_color=theme["btn_hover"],
                                  text_color=theme["fg"],
                                  command=lambda: SettingsPanel(self))
        config_btn.pack(side="left", padx=5)
        
        # Estadísticas
        stats_btn = ctk.CTkButton(tools_frame, text="📊", width=50,
                                 fg_color=theme["btn_bg"],
                                 hover_color=theme["btn_hover"],
                                 text_color=theme["fg"],
                                 command=lambda: StatsPanel(self, self.data_manager))
        stats_btn.pack(side="left", padx=5)
        
        # Exportar
        export_btn = ctk.CTkButton(tools_frame, text="📄", width=50,
                                  fg_color=theme["btn_bg"],
                                  hover_color=theme["btn_hover"],
                                  text_color=theme["fg"],
                                  command=self.show_export_menu)
        export_btn.pack(side="left", padx=5)
        
        # Información del usuario
        user_frame = ctk.CTkFrame(self, fg_color="transparent")
        user_frame.pack(fill="x", padx=20, pady=10)
        
        # Nivel y puntos
        self.level_var = ctk.StringVar(value=f"Nivel {self.user_data['level']}")
        level_label = ctk.CTkLabel(user_frame, textvariable=self.level_var,
                                  font=small_font, text_color=theme["fg"])
        level_label.pack(side="left")
        
        self.points_var = ctk.StringVar(value=f"Puntos: {self.user_data['total_points']}")
        points_label = ctk.CTkLabel(user_frame, textvariable=self.points_var,
                                   font=small_font, text_color=theme["fg"])
        points_label.pack(side="right")
    
    def show_export_menu(self):
        """Mostrar menú de exportación"""
        export_window = ctk.CTkToplevel(self)
        export_window.title("Exportar Reportes")
        export_window.geometry("300x200")
        export_window.configure(fg_color=self.current_theme["bg"])
        
        ctk.CTkLabel(export_window, text="Exportar Reportes",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.current_theme["fg"]).pack(pady=20)
        
        pdf_btn = ctk.CTkButton(export_window, text="📄 Exportar PDF",
                               fg_color=self.current_theme["btn_bg"],
                               hover_color=self.current_theme["btn_hover"],
                               text_color=self.current_theme["fg"],
                               command=self.export_pdf)
        pdf_btn.pack(pady=10)
        
        csv_btn = ctk.CTkButton(export_window, text="📊 Exportar CSV",
                               fg_color=self.current_theme["btn_bg"],
                               hover_color=self.current_theme["btn_hover"],
                               text_color=self.current_theme["fg"],
                               command=self.export_csv)
        csv_btn.pack(pady=10)
    
    def export_pdf(self):
        """Exportar reporte PDF"""
        filename = self.report_exporter.export_pdf_report()
        if filename:
            webbrowser.open(filename)
    
    def export_csv(self):
        """Exportar datos CSV"""
        filename = self.report_exporter.export_csv_data()
        if filename:
            os.startfile(filename)
    
    def _start(self):
        """Iniciar/pausar timer"""
        if not self.running:
            self.running = True
            self.start_btn.configure(text="⏸ PAUSE")
            self.session_start_time = time.time()
            self.sound_manager.play_start_sound()
            self._countdown()
        else:
            self.running = False
            self.start_btn.configure(text="▶ START")
            self.sound_manager.play_pause_sound()
            self.pause_start_time = time.time()
            self.start_pause_penalty()
    
    def start_pause_penalty(self):
        """Penalización por pausa"""
        def penalty_thread():
            while not self.running and self.pause_start_time:
                time.sleep(10)
                if not self.running and self.pause_start_time:
                    self.user_data["total_points"] = max(0, self.user_data["total_points"] - 1)
                    self.after(0, self.update_display)
        
        self.pause_thread = threading.Thread(target=penalty_thread, daemon=True)
        self.pause_thread.start()
    
    def _countdown(self):
        """Cuenta regresiva principal"""
        if self.running:
            if self.remaining <= 0:
                self.complete_session()
            else:
                self.remaining -= 1
                self._update_label()
                self.after(1000, self._countdown)
    
    def complete_session(self):
        """Completar sesión y dar recompensas"""
        self.running = False
        self.start_btn.configure(text="▶ START")
        
        # Reproducir sonido
        self.sound_manager.play_completion_sound()
        
        # Solo dar recompensas si no hubo pausas
        if self.pause_start_time is None:
            # Calcular duración de la sesión
            session_duration = self.WORK_MIN if self.current_session_type == "work" else self.BREAK_MIN
            
            # Registrar sesión
            self.data_manager.log_session(self.current_session_type, session_duration, True)
            
            # Dar puntos y experiencia
            points = 10 if self.current_session_type == "work" else 5
            self.user_data["total_points"] += points
            self.user_data["total_focus_time"] += session_duration
            self.user_data["completed_sessions"] += 1
            self.achievement_system.add_experience(points)
            
            # Actualizar estadísticas diarias
            today = dt.datetime.now().strftime("%Y-%m-%d")
            if today not in self.user_data["daily_stats"]:
                self.user_data["daily_stats"][today] = 0
            self.user_data["daily_stats"][today] += 1
            
            # Verificar logros
            new_achievements = self.achievement_system.check_achievements(None)
            if new_achievements:
                self.show_achievement_notification(new_achievements)
            
            # Guardar datos
            self.data_manager.save_user_data(self.user_data)
        
        # Cambiar tipo de sesión
        if self.current_session_type == "work":
            self.current_session_type = "break"
            self.remaining = self.BREAK_MIN * 60
            self.session_var.set("Descanso")
        else:
            self.current_session_type = "work"
            self.remaining = self.WORK_MIN * 60
            self.session_var.set("Trabajo")
        
        self.pause_start_time = None
        self._update_label()
        self.update_display()
    
    def show_achievement_notification(self, achievements):
        """Mostrar notificación de logros"""
        notification = ctk.CTkToplevel(self)
        notification.title("¡Logro Desbloqueado!")
        notification.geometry("300x150")
        notification.configure(fg_color=self.current_theme["bg"])
        notification.attributes("-topmost", True)
        
        for achievement_key in achievements:
            achievement = AchievementSystem.ACHIEVEMENTS[achievement_key]
            
            ctk.CTkLabel(notification, text=achievement["icon"],
                        font=ctk.CTkFont(size=48)).pack(pady=10)
            
            ctk.CTkLabel(notification, text=f"¡{achievement['name']}!",
                        font=ctk.CTkFont(size=16, weight="bold"),
                        text_color=self.current_theme["fg"]).pack()
            
            ctk.CTkLabel(notification, text=achievement["desc"],
                        text_color=self.current_theme["fg"]).pack()
        
        # Auto-cerrar después de 3 segundos
        notification.after(3000, notification.destroy)
    
    def update_display(self):
        """Actualizar display de puntos y nivel"""
        self.points_var.set(f"Puntos: {self.user_data['total_points']}")
        self.level_var.set(f"Nivel {self.user_data['level']}")
    
    def _reset(self):
        """Resetear timer"""
        self.running = False
        self.current_session_type = "work"
        self.remaining = self.WORK_MIN * 60
        self.start_btn.configure(text="▶ START")
        self.session_var.set("Trabajo")
        self.pause_start_time = None
        self._update_label()
    
    def _update_label(self):
        """Actualizar display del timer"""
        m, s = divmod(self.remaining, 60)
        self.timer_var.set(f"{m:02}:{s:02}")

if __name__ == "__main__":
    app = Pomodoro()
    app.mainloop()
