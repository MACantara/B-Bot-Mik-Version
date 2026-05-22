# B-Bot: Command-Based City-Building Simulation

A command-based city-building simulation game where you control a robot (B-Bot) using Python scripts to harvest resources and build structures.

## Tech Stack

### Backend
- Flask (Python 3.10+)
- RestrictedPython (secure script execution)
- Supabase Python Client
- PostgreSQL (via Supabase)
- JWT authentication with refresh tokens
- Flask-CORS

### Frontend
- Jinja2 templates (server-side rendering)
- Three.js (3D grid visualization)
- Tailwind CSS (via CDN)
- Custom JavaScript for game logic

## Project Structure

```
B-Bot/
├── core/                     # Core application logic
│   ├── interpreter/          # RestrictedPython script interpreter
│   │   ├── script_interpreter.py
│   │   ├── simulator.py
│   │   ├── bot_command.py
│   │   ├── safe_globals.py
│   │   └── exceptions.py
│   ├── config.py             # Configuration
│   ├── database.py           # Supabase database
│   └── security.py           # JWT authentication
├── routes/                   # Flask blueprints
│   ├── auth.py               # Authentication endpoints
│   └── simulation.py        # Game simulation endpoints
├── templates/                # Jinja2 templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── game.html
├── static/                   # Static assets
│   ├── js/game/              # Game JavaScript
│   └── css/                  # Stylesheets
├── tests/                    # Test suite
│   ├── test_website.py
│   ├── test_interpreter_functionality.py
│   ├── test_interpreter_security.py
│   └── test_dsl.py
├── docs/                     # Documentation
├── wsgi.py                   # WSGI entry point
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel deployment config
├── .env.example              # Environment variables template
└── README.md
```

## Features

### Game Mechanics
- **20x20 Grid Map**: Visual city map with trees, rocks, empty plots, and buildings
- **Five Command Primitives**:
  - `bot.move()` - Move robot forward in current direction
  - `bot.turn_left()` - Rotate 90 degrees counter-clockwise
  - `bot.turn_right()` - Rotate 90 degrees clockwise
  - `bot.harvest()` - Gather resources (wood from trees, stone from rocks)
  - `bot.build(type)` - Build structure (costs 2 wood + 1 stone)
- **Resource Tracking**: Wood, Stone, Metal, Energy
- **Real-time Animation**: Visual command execution with step-by-step feedback
- **Timeout Protection**: 5-second execution limit to prevent infinite loops

### Scripting
- **Full Python Support**: Write real Python scripts using RestrictedPython
- **Variables & Arithmetic**: Use variables and mathematical operations
- **Control Flow**: for loops, while loops, if statements
- **Functions**: Define and call custom functions
- **Data Structures**: Lists, dictionaries, tuples
- **Secure Execution**: Sandboxed environment with RestrictedPython

### Authentication
- JWT-based authentication with access and refresh tokens
- User registration and login endpoints
- Token refresh mechanism
- Protected API endpoints

### Data Persistence
- Save game state to PostgreSQL database
- Store exact grid configuration (all cell types and positions)
- Track resource counts and population
- User-specific save states

## Documentation

For detailed documentation, see the [docs/](docs/) folder:
- [User Guide](docs/user-guide.md) - How to play the game
- [Architecture](docs/architecture.md) - System design and data flow
- [API Reference](docs/api.md) - Complete API documentation
- [Scripting Guide](docs/scripting-guide.md) - Python scripting reference
- [Security](docs/security.md) - Security model and sandbox details
- [Deployment](docs/deployment.md) - Setup and deployment instructions
- [Testing](docs/testing.md) - Test structure and running tests
- [Contributing](docs/contributing.md) - Development guidelines

## Quick Start

### Prerequisites
- Python 3.10+
- Supabase account (for PostgreSQL database)

### Installation

1. Clone the repository
2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
- **Windows**: `copy .env.example .env`
- **macOS/Linux**: `cp .env.example .env`

6. Update `.env` with your Supabase credentials:
```
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

7. Set up Supabase database:
   - Open your Supabase project dashboard
   - Navigate to the SQL Editor
   - Run the SQL script from `supabase_setup.sql`

8. Run development server:
```bash
python wsgi.py
```

The application will be available at `http://localhost:5000`

## Deployment

### Vercel

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

## License

MIT
