# System Architecture

Overview of the B-Bot system architecture, components, and data flow.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Browser                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Three.js   │  │  Skulpt.js   │  │   Jinja2     │         │
│  │  (3D Grid)   │  │  (Python     │  │  Templates   │         │
│  │              │  │   Interpreter)│              │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         │                  ▼                  │                 │
│         │         ┌──────────────┐           │                 │
│         │         │ Animation    │           │                 │
│         │         │   Engine     │           │                 │
│         │         └──────┬───────┘           │                 │
│         │                │                  │                 │
│         └────────────────┴──────────────────┘                 │
│                            │                                     │
│                            ▼                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │ HTTP/JSON (save/load only)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask Backend Server                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Routes     │  │   Security   │  │   Database   │         │
│  │  (auth/sim)  │  │   (JWT)      │  │  (Supabase)  │         │
│  │              │  │              │  │              │         │
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

#### Skulpt.js (Python Interpreter)
- Executes Python scripts directly in the browser
- Configured for Python 3 behavior
- Provides FFI bridge for bot object
- Generates command queue for animation
- Browser sandboxed execution (no server code execution)

#### Animation Engine
- Processes command queue with smooth animations
- Implements lerp-based interpolation for movement
- Handles turn, harvest, and build animations
- Uses requestAnimationFrame for smooth rendering
- Separates command execution from animation

#### Three.js (3D Visualization)
- Renders the 20x20 grid in 3D
- Displays cell types (trees, rocks, buildings, empty)
- Animates robot movement and actions
- Handles user camera controls

#### JavaScript (Game Logic)
- Manages game state locally
- Handles command queue execution
- Updates UI in real-time
- Communicates with Flask backend for save/load only

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
  - Save game state (requires auth)
  - Load game state (requires auth)
  - Note: Execute endpoint removed (now client-side)

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

### Script Execution Flow (Client-Side)

```
User Script
     │
     ▼
┌─────────────────┐
│  Skulpt.js      │  Execute Python in browser
│  Interpreter     │  Python 3 mode enabled
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Bot Object FFI  │  Map bot methods to JS
│  Bridge         │  Generate command queue
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Command Queue   │  [MOVE, TURN_LEFT, HARVEST, BUILD]
│  Generation     │  Pure JavaScript array
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Animation       │  Process with lerp interpolation
│  Engine         │  Smooth visual updates
└────────┬────────┘
         │
         ▼
Three.js Rendering
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

### Client-Side Browser Sandbox

```
User Script
     │
     ▼
┌─────────────────┐
│  Skulpt.js      │  Execute in browser sandbox
│  Interpreter     │  No server code execution
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Browser        │  Isolated execution context
│  Sandbox        │  No file system access
└────────┬────────┘
         │
         ▼
Command Queue
```

### Security Layers

1. **Browser Sandbox**
   - Scripts execute in isolated browser context
   - No server code execution risk
   - No file system access
   - No network access to internal systems

2. **Skulpt.js Configuration**
   - Python 3 mode enabled
   - File I/O blocked
   - Import statements blocked
   - Safe built-in functions only

3. **Authentication**
   - JWT token validation
   - Protected save/load endpoints
   - Token refresh mechanism

4. **Server-Side Validation**
   - Input validation on save/load
   - Rate limiting on API endpoints
   - Supabase RLS policies for data access

## File Structure

```
core/
├── config.py                    # Configuration
├── database.py                  # Supabase client
└── security.py                  # JWT authentication

routes/
├── auth.py                      # Authentication endpoints
└── simulation.py                # Save/load endpoints

templates/
├── base.html                    # Base template
├── login.html                   # Login page
├── register.html                # Registration page
└── game.html                    # Game interface

static/
├── js/
│   ├── game/
│   │   ├── main.js              # Game initialization
│   │   ├── commands.js          # Command processing
│   │   ├── animation.js         # Animation engine
│   │   ├── bot.js               # Bot state management
│   │   ├── grid.js              # Grid rendering
│   │   ├── resources.js         # Resource tracking
│   │   ├── console.js           # Console output
│   │   └── storage.js           # Save/load handling
│   └── interpreter/
│       └── skulpt-bridge.js     # Skulpt.js FFI bridge
└── css/                         # Stylesheets
```

## Technology Stack

### Backend
- **Flask** - Web framework
- **Supabase** - Database and auth
- **PostgreSQL** - Relational database
- **PyJWT** - JWT token handling

### Frontend
- **Skulpt.js** - Client-side Python interpreter
- **Three.js** - 3D graphics
- **Jinja2** - Template engine
- **Tailwind CSS** - Styling
- **Vanilla JavaScript** - Game logic

### Deployment
- **Vercel** - Hosting platform
- **WSGI** - Python web server interface
