# B-Bot: Command-Based City-Building Simulation

A command-based city-building simulation game where you control a robot (B-Bot) using Python-like scripts to harvest resources and build structures.

## Tech Stack

### Frontend
- React (Vite-based)
- TypeScript
- Tailwind CSS
- Zustand (state management)
- @uiw/react-codemirror (code editor with Python syntax highlighting)

### Backend
- FastAPI (Python 3.10+)
- Pydantic v2
- Supabase Python Client
- PostgreSQL (via Supabase)
- JWT authentication with refresh tokens

## Project Structure

```
B-Bot/
├── frontend/                 # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/       # UI components (Grid, Editor, Dashboard, Console)
│   │   ├── store/           # Zustand store
│   │   ├── interpreter/     # AST parser and executor
│   │   └── types/           # TypeScript interfaces
│   ├── vercel.json          # Vercel deployment config
│   └── .env.example         # Environment variables template
├── backend/                  # FastAPI + Python
│   ├── app/
│   │   ├── api/             # API endpoints (auth, simulation)
│   │   ├── core/            # Security, config, database
│   │   └── schemas/         # Pydantic schemas
│   ├── main.py              # FastAPI application entry point
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
- Node.js 18+
- Python 3.10+
- Supabase account (for PostgreSQL database)

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
- **Windows**: `copy .env.example .env`
- **macOS/Linux**: `cp .env.example .env`

4. Update `.env` with your API URL:
```
VITE_API_URL=http://localhost:8000
```

5. Run development server:
```bash
npm run dev
```

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
   - This will create the `users` and `save_states` tables with appropriate RLS policies

8. Run development server:
```bash
uvicorn main:app --reload
```

## Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variable: `VITE_API_URL` (your deployed backend URL)
4. Deploy

### Backend (Vercel)

1. Push code to GitHub
2. Create a new Vercel project from the `backend` directory
3. Set environment variables:
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon/public key
   - `SECRET_KEY` - Your JWT secret key
4. Deploy

### Alternative Backend Deployment (Railway, Render, etc.)

1. Deploy FastAPI app to your preferred hosting platform
2. Set environment variables (SUPABASE_URL, SUPABASE_KEY, SECRET_KEY)
3. Run the `supabase_setup.sql` script in your Supabase SQL Editor
4. Update frontend `VITE_API_URL` to point to production backend

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
