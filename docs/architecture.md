# System Architecture

Overview of the B-Bot system architecture, components, and data flow.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Browser                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Three.js   │  │  JavaScript  │  │   Jinja2     │         │
│  │  (3D Grid)   │  │  (Game Logic)│  │  Templates   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                     │
│                            ▼                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │ HTTP/JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask Backend Server                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Routes     │  │  Interpreter │  │  Simulator   │         │
│  │  (auth/sim)  │  │ (Restricted  │  │  (Game Logic) │         │
│  │              │  │   Python)    │  │              │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Security   │  │   Database   │  │   Config     │         │
│  │   (JWT)      │  │  (Supabase)  │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supabase PostgreSQL                          │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │    users     │  │ save_states  │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## Component Overview

### Frontend Components

#### Three.js (3D Visualization)
- Renders the 20x20 grid in 3D
- Displays cell types (trees, rocks, buildings, empty)
- Animates robot movement and actions
- Handles user camera controls

#### JavaScript (Game Logic)
- Manages game state locally
- Handles command queue execution
- Updates UI in real-time
- Communicates with Flask backend via fetch API

#### Jinja2 Templates
- Server-side rendered HTML
- Provides initial page structure
- Includes authentication state
- Loads static assets

### Backend Components

#### Flask Routes
- **Authentication Blueprint** (`/api/auth/*`)
  - User registration
  - User login
  - Token refresh
- **Simulation Blueprint** (`/api/simulation/*`)
  - Get initial grid state
  - Execute user scripts
  - Save/load game state

#### Script Interpreter
- **RestrictedPython Integration**
  - Compiles user scripts safely
  - Enforces security restrictions
  - Executes in sandboxed environment
- **BotCommand Class**
  - Captures bot actions
  - Generates command queue
  - Tracks execution state
- **Safe Globals**
  - Provides safe built-in functions
  - Blocks dangerous operations
  - Includes guard functions

#### Simulator
- **Command Execution**
  - Processes command queue
  - Updates game state
  - Calculates resource changes
- **Game Logic**
  - Movement validation
  - Resource collection
  - Building placement
  - Boundary checking

#### Security
- **JWT Authentication**
  - Access token generation
  - Refresh token management
  - Token validation middleware
- **Password Hashing**
  - Secure password storage
  - Verification on login

#### Database (Supabase)
- **PostgreSQL Database**
  - User accounts
  - Save states
  - Game progress
- **Supabase Client**
  - Python ORM interface
  - Query execution
  - Connection management

## Data Flow

### Script Execution Flow

```
User Script
     │
     ▼
┌─────────────────┐
│  Flask Route    │  POST /api/simulation/execute
│  (execute)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Script          │  Parse and validate script
│ Interpreter     │  Compile with RestrictedPython
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Command Queue   │  Extract bot commands
│ Generation      │  [MOVE, TURN_LEFT, HARVEST, BUILD]
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Simulator       │  Execute commands
│ Execution       │  Update game state
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Detailed Queue  │  Add metadata (positions, resources)
│ Generation      │  Return to frontend
└────────┬────────┘
         │
         ▼
Frontend Animation
```

### Authentication Flow

```
User Credentials
     │
     ▼
┌─────────────────┐
│  Flask Route    │  POST /api/auth/login
│  (login)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Security       │  Verify password hash
│  Module         │  Generate JWT tokens
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Database       │  Query user record
│  (Supabase)     │
└────────┬────────┘
         │
         ▼
Response: Access Token + Refresh Token
```

### Save/Load Flow

```
Game State
     │
     ▼
┌─────────────────┐
│  Flask Route    │  POST /api/simulation/save
│  (save)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Database       │  Insert/Update save_states
│  (Supabase)     │
└────────┬────────┘
         │
         ▼
Response: Save Confirmation
```

## Security Model

### RestrictedPython Sandbox

```
User Script
     │
     ▼
┌─────────────────┐
│  AST Import     │  Block import statements
│  Check          │  at compile time
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Restricted     │  Compile with safe globals
│  Python         │  Apply guard functions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Safe Globals   │  Block dangerous built-ins
│  Environment    │  Provide safe functions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Multiprocess   │  Execute in separate process
│  Worker         │  5-second timeout
└────────┬────────┘
         │
         ▼
Command Queue
```

### Security Layers

1. **AST-Level Blocking**
   - Import statements blocked before compilation
   - Syntax validation

2. **RestrictedPython Compilation**
   - Rewrites dangerous operations
   - Applies guard functions
   - Limits attribute access

3. **Safe Globals**
   - Blocks: __builtins__, eval, exec, compile, open
   - Provides: safe_builtins, _getiter_, _iter_unpack_sequence_
   - Guards: _getattr_, _write_, _import_

4. **Timeout Protection**
   - Multiprocessing isolation
   - 5-second execution limit
   - Prevents infinite loops

5. **Authentication**
   - JWT token validation
   - Protected endpoints
   - Token refresh mechanism

## File Structure

```
core/
├── interpreter/
│   ├── script_interpreter.py    # Main interpreter class
│   ├── simulator.py              # Game logic simulator
│   ├── bot_command.py            # Command capture
│   ├── safe_globals.py           # Safe environment
│   └── exceptions.py            # Custom exceptions
├── config.py                    # Configuration
├── database.py                  # Supabase client
└── security.py                  # JWT authentication

routes/
├── auth.py                      # Authentication endpoints
└── simulation.py                # Game simulation endpoints

templates/
├── base.html                    # Base template
├── login.html                   # Login page
├── register.html                # Registration page
└── game.html                    # Game interface

static/
├── js/game/
│   └── main.js                  # Game JavaScript
└── css/                         # Stylesheets
```

## Technology Stack

### Backend
- **Flask** - Web framework
- **RestrictedPython** - Secure script execution
- **Supabase** - Database and auth
- **PostgreSQL** - Relational database
- **PyJWT** - JWT token handling

### Frontend
- **Three.js** - 3D graphics
- **Jinja2** - Template engine
- **Tailwind CSS** - Styling
- **Vanilla JavaScript** - Game logic

### Deployment
- **Vercel** - Hosting platform
- **WSGI** - Python web server interface
