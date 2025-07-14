import os
import json

def create_project_structure():
    """Crear estructura completa del proyecto con archivos JSON"""
    
    # Crear directorios
    directories = [
        "pomodoro_data",
        "themes", 
        "sounds",
        "exports",
        "backups"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directorio creado: {directory}")
    
    # Crear archivos JSON por defecto
    create_default_files()
    print("🎉 ¡Estructura del proyecto creada exitosamente!")

def create_default_files():
    """Crear archivos JSON con configuración por defecto"""
    
    # settings.json
    settings = {
        "work_time": 25,
        "break_time": 5,
        "theme": "Terminal",
        "sound_enabled": True,
        "sound_volume": 75
    }
    
    with open("pomodoro_data/settings.json", "w") as f:
        json.dump(settings, f, indent=2)
    
    # user_data.json
    user_data = {
        "total_points": 0,
        "level": 1,
        "experience": 0,
        "completed_sessions": 0,
        "total_focus_time": 0,
        "achievements": [],
        "daily_stats": {}
    }
    
    with open("pomodoro_data/user_data.json", "w") as f:
        json.dump(user_data, f, indent=2)
    
    # sessions.json (array vacío)
    with open("pomodoro_data/sessions.json", "w") as f:
        json.dump([], f, indent=2)

if __name__ == "__main__":
    create_project_structure()
