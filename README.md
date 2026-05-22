# B-Bot: Command-Based City-Building Simulation

A command-based city-building simulation game where you control a robot (B-Bot) using Python-like scripts to harvest resources and build structures.

## Tech Stack

### Backend & Frontend (Flask + Jinja2)
- Flask (Python 3.10+)
- Jinja2 templates (server-side rendering)
- Tailwind CSS (via CDN)
- Supabase Python Client
- PostgreSQL (via Supabase)
- JWT authentication with refresh tokens
- Flask-CORS

## Project Structure

```
B-Bot/
├── backend/                  # Flask + Python
│   ├── app/
│   │   ├── routes/          # Flask blueprints (auth, simulation)
│   │   ├── core/            # Security, database
│   │   └── templates/       # Jinja2 templates
│   ├── wsgi.py              # WSGI entry point
│   ├── vercel.json          # Vercel deployment config
│   └── .env.example         # Environment variables template
└── README.md
```

## Features

### Game Mechanics
- **10x10 Grid Map**: Visual city map with trees, rocks, empty plots, and houses
- **Four Command Primitives**:
  - `bbot.move()` - Move robot forward in current direction
  - `bbot.turn()` - Rotate 90 degrees clockwise
  - `bbot.harvest()` - Gather resources (wood from trees, stone from rocks)
  - `bbot.build()` - Build house (costs 2 wood + 1 stone)
- **Resource Tracking**: Wood, Stone, Population, Energy
- **Real-time Animation**: 300ms delay between commands for visual feedback
- **Execution Limit**: Maximum 500 steps to prevent infinite loops

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

## Setup Instructions

### Prerequisites
- Python 3.10+
- Supabase account (for PostgreSQL database)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

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

To get your Supabase credentials:
1. Go to your Supabase project dashboard
2. Navigate to Settings → API
3. Copy the Project URL
4. Copy the **anon/public** key (NOT the publishable key - the anon key starts with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

To generate a secure secret key, run:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

7. Set up Supabase database tables:
   - Open your Supabase project dashboard
   - Navigate to the SQL Editor
   - Open the `supabase_setup.sql` file from the backend directory
   - Copy and paste the SQL script into the SQL Editor
   - Click "Run" to execute the script
   - This will create the `users` and `save_states` tables

8. Run development server:
```bash
python wsgi.py
```

The application will be available at `http://localhost:5000`

## Deployment

### Vercel (Single Project)

1. Push code to GitHub
2. Import project in Vercel from the `backend` directory
3. Set environment variables:
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon/public key
   - `SECRET_KEY` - Your JWT secret key
4. Deploy

The application will be deployed as a single Flask application with server-side rendering.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/refresh` - Refresh access token

### Simulation
- `GET /api/simulation/state` - Get demo 10x10 grid configuration
- `POST /api/simulation/save` - Save game state (requires auth)
- `GET /api/simulation/save` - Get saved game state (requires auth)

## Game Commands

Write Python-like scripts in the code editor:

```python
bbot.move()
bbot.move()
bbot.turn()
bbot.move()
bbot.harvest()
bbot.turn()
bbot.move()
bbot.build()
```

Click "Run Code" to execute the script and watch B-Bot navigate the grid, harvest resources, and build structures.

## License

MIT
