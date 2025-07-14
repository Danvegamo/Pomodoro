# 🍅 Pomodoro Pro - Retro Gamified Productivity Timer

<div align="center">
    <img src="assets/logo.png" alt="Pomodoro Pro Logo" width="200"/>


**Pomodoro Pro** is a comprehensive productivity timer application born from frustration with existing Pomodoro tools that lacked the features I needed as a visual artist and environmental researcher. As someone who works on immersive art projects, climate change initiatives, and indigenous community collaborations, I required a tool that could adapt to my unique workflow patterns while maintaining motivation through gamification.
</div>
---

### 👨‍🎨 About the Creator

I'm **David Vega**, a visual artist specialized in immersive art projects working for climate change and with indigenous communities. I combine my passion for:
- **Environmental Research**: Advising climate change projects at global standards
- **Immersive Storytelling**: Creating processes that connect people with environmental narratives
- **Academic Excellence**: Teaching at Colombia's top universities
- **Technology Innovation**: Exploring new programming technologies and their applications
- **Financial Literacy**: Understanding economic systems that impact environmental projects

This application represents my journey into software development, serving both as a practical tool for my research work and a learning experience in Git workflows and open-source collaboration.

## 🚀 Why Pomodoro Pro?

After searching extensively for a Pomodoro timer that could:
- **Stay minimized** without being distracting during focus sessions
- **Adapt to different work patterns** (research, creative work, teaching preparation)
- **Provide meaningful statistics** for productivity analysis
- **Gamify the experience** to maintain long-term motivation
- **Export professional reports** for academic documentation

I realized I needed to build my own solution. This project also serves as my introduction to **open-source development** and **collaborative coding**, welcoming contributions from the community.

## ✨ Features

### 🎮 Gamification System
- **Experience Points & Leveling**: Earn XP for completed sessions
- **Achievement System**: Unlock 10+ unique badges
- **Smart Penalty System**: Lose points for excessive pausing
- **Progress Tracking**: Visual progression indicators

### 🎨 Customization
- **4 Retro Themes**: Terminal, Matrix, Cyberpunk, Retro Amber
- **Flexible Timing**: Auto-adjusting break times (20% of work time)
- **Sound Notifications**: Custom 8-bit audio cues
- **Always-on-Top**: Unobtrusive mini-timer mode

### 📊 Analytics & Reporting
- **Real-time Statistics**: Daily, weekly, and monthly insights
- **Visual Charts**: Matplotlib integration for productivity graphs
- **Export Options**: PDF reports and CSV data
- **Session Logging**: Complete history with tags and notes

### 🔧 Technical Features
- **Data Persistence**: JSON-based storage system
- **Cross-platform**: Windows, macOS, Linux support
- **Lightweight**: Minimal resource usage
- **Extensible**: Theme and plugin system

## 📋 Prerequisites

- **Python 3.10+**
- **Git** (for cloning and contributing)
- **Basic command line knowledge**

## 🛠️ Installation

### Option 1: Quick Start (Recommended)
```bash
# Clone the repository
git clone https://github.com/danvegamo/pomodoro-pro.git
cd pomodoro-pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up project structure
python setup_files.py

# Run the application
python pomodoro_pro.py
```

### Option 2: Standalone Executable
1. Download the latest release from [Releases](https://github.com/danvegamo/pomodoro-pro/releases)
2. Extract and run `PomodoroProV2.exe`

## 🎵 Audio Setup

### Custom Sound Generation
The application uses custom 8-bit retro sounds. You can:

1. **Use default sounds** (included in repository)
2. **Generate custom sounds** using [Suno.ai](https://suno.ai) with these prompts:

**Start Sound**: *"Create a short 8-bit retro video game sound effect for starting a focus session, uplifting and motivational chiptune melody with rising notes, bright synthesizer tones, duration 2-3 seconds, similar to classic arcade game power-up sounds, energetic and encouraging feel."*

**Complete Sound**: *"Generate a triumphant 8-bit victory sound effect for completing a pomodoro session, celebratory chiptune melody with ascending arpeggios, classic arcade achievement sound, bright and satisfying synthesizer notes, duration 3-4 seconds, reminiscent of retro game level completion."*

**Pause Sound**: *"Design a gentle 8-bit notification sound for pausing a timer, soft chiptune melody with descending tones, calming retro game sound effect, mellow synthesizer notes, duration 1-2 seconds, friendly and non-intrusive audio cue for break time."*

3. **Place audio files** in `sounds/` directory as `.wav` files

## 🎨 Assets & Images

### Required Assets
- **Logo**: `assets/logo.png` (256x256px recommended)
- **Icon**: `icon.ico` (for Windows executable)
- **Screenshots**: `screenshots/` directory for documentation

### Image Guidelines
- **Format**: PNG preferred, ICO for Windows icons
- **Resolution**: 256x256px for icons, 1920x1080px for screenshots
- **Style**: Retro/8-bit aesthetic to match application theme
- **Colors**: Match the selected theme palette

### Creating Assets
1. **Logo**: Use the provided Pomodoro + Snake 8-bit style
2. **Screenshots**: Capture different themes and features
3. **Icons**: Create variations for different platforms

## 🗂️ Project Structure

```
pomodoro-pro/
├── pomodoro_pro.py          # Main application
├── setup_files.py           # Project initialization
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
├── assets/
│   ├── logo.png           # Application logo
│   └── screenshots/       # Feature screenshots
├── sounds/
│   ├── start.wav          # Session start sound
│   ├── complete.wav       # Session completion sound
│   ├── pause.wav          # Pause notification
│   └── reset.wav          # Reset sound
├── themes/
│   ├── terminal.json      # Terminal theme
│   ├── matrix.json        # Matrix theme
│   ├── cyberpunk.json     # Cyberpunk theme
│   └── retro_amber.json   # Retro Amber theme
├── pomodoro_data/         # User data (auto-generated)
│   ├── settings.json      # User preferences
│   ├── user_data.json     # Progress and achievements
│   └── sessions.json      # Session history
└── dist/                  # Compiled executables
```

## 🎯 Usage

### Basic Operation
1. **Launch** the application
2. **Set your work time** (default: 25 minutes)
3. **Click START** to begin your focus session
4. **Take breaks** when prompted
5. **Track your progress** in the statistics panel

### Advanced Features
- **Mini-Timer Mode**: Click minimize to get a corner timer
- **Theme Switching**: Access via settings gear icon
- **Statistics**: View detailed productivity analytics
- **Export Reports**: Generate PDF summaries of your work patterns

## 🛣️ Roadmap

### Phase 1: Foundation ✅
- [x] Core Pomodoro functionality
- [x] Gamification system
- [x] Theme system
- [x] Basic statistics

### Phase 2: Enhancement (Current)
- [ ] **Cloud Sync**: Synchronize data across devices
- [ ] **Team Features**: Collaborative productivity tracking
- [ ] **Advanced Analytics**: AI-powered insights
- [ ] **Mobile Companion**: Smartphone integration

### Phase 3: Community & Integration
- [ ] **Plugin System**: Community-developed extensions
- [ ] **API Development**: Integration with other productivity tools
- [ ] **Multi-language Support**: Localization for global use
- [ ] **Environmental Impact**: Carbon footprint tracking for digital work

### Phase 4: Research Integration
- [ ] **Academic Tools**: Citation management integration
- [ ] **Research Patterns**: Specialized workflows for academic work
- [ ] **Collaboration Tools**: Features for indigenous community projects
- [ ] **Impact Measurement**: Quantify productivity improvements

## 🤝 Contributing

I welcome contributions from developers, designers, and productivity enthusiasts! This project serves as my learning ground for collaborative development.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** your changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to the branch: `git push origin feature/AmazingFeature`
5. **Open** a Pull Request

### What We Need
- **🐛 Bug Reports**: Help identify and fix issues
- **✨ Feature Requests**: Suggest new functionality
- **🎨 UI/UX Design**: Improve the visual experience
- **📚 Documentation**: Enhance guides and tutorials
- **🌐 Translations**: Multi-language support
- **🔊 Audio Design**: Better sound effects and themes

### Contribution Guidelines
- **Follow** existing code style
- **Add** tests for new features
- **Update** documentation
- **Be respectful** and constructive in discussions

## 📊 Technical Stack

- **Frontend**: CustomTkinter (Python)
- **Data Storage**: JSON files
- **Analytics**: Matplotlib, Pandas
- **Audio**: Windows Sound API
- **Reports**: ReportLab PDF generation
- **Packaging**: PyInstaller

## 🐛 Known Issues

- **Windows Only**: Full sound support currently Windows-specific
- **Large Files**: PDF reports can be large with extensive data
- **Theme Switching**: Requires application restart for some themes

## 💬 Community & Support

- **Issues**: [GitHub Issues](https://github.com/danvegamo/pomodoro-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/danvegamo/pomodoro-pro/discussions)
- **Email**: [daniel.vega@environment.art](mailto:daniel.vega@environment.art)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pomodoro Technique**: Francesco Cirillo
- **Open Source Community**: For inspiration and tools
- **Indigenous Communities**: For teaching sustainable time practices
- **Environmental Researchers**: For showing the importance of focused work
- **Students**: For testing and feedback during development

## 🌱 Environmental Impact

As someone working on climate change projects, I'm committed to:
- **Efficient Code**: Minimal resource usage
- **Digital Minimalism**: Reducing screen time through focused work
- **Open Source**: Preventing duplicate development efforts
- **Educational Value**: Teaching sustainable productivity practices

<div align="center">
  
**Built with ❤️ for focused, sustainable productivity**

*Supporting environmental research, one pomodoro at a time*

</div>