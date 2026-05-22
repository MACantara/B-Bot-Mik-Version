# API Reference

Complete API documentation for the B-Bot backend endpoints.

## Base URL

```
http://localhost:5000/api
```

## Authentication

Most endpoints require JWT authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication Endpoints

#### Register User

Register a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Username already exists"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "password": "securepassword123"}'
```

#### Login

Authenticate and receive access and refresh tokens.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "password": "securepassword123"}'
```

#### Refresh Token

Refresh an expired access token using a refresh token.

**Endpoint:** `POST /auth/refresh`

**Request Body:**
```json
{
  "refresh_token": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid refresh token"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

### Simulation Endpoints

#### Get Simulation State

Get the initial demo 20x20 grid configuration.

**Endpoint:** `GET /simulation/state`

**Authentication:** Not required

**Response (200 OK):**
```json
{
  "grid": [
    [
      {"type": "EMPTY", "id": "0-0"},
      {"type": "TREE", "id": "1-0"},
      {"type": "ROCK", "id": "2-0"}
    ]
  ],
  "bot": {
    "x": 0,
    "y": 0,
    "direction": "RIGHT",
    "inventory": {
      "wood": 0,
      "stone": 0,
      "metal": 0,
      "energy": 0
    }
  },
  "population": 0,
  "resources": {
    "wood": 0,
    "stone": 0,
    "metal": 0,
    "energy": 0
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/simulation/state
```

#### Execute Script

Execute a user script and return the command queue and final game state.

**Endpoint:** `POST /simulation/execute`

**Authentication:** Required

**Request Body:**
```json
{
  "script": "bot.move()\nbot.harvest()",
  "grid": [
    [
      {"type": "EMPTY", "id": "0-0"},
      {"type": "TREE", "id": "1-0"}
    ]
  ],
  "bot": {
    "x": 0,
    "y": 0,
    "direction": "RIGHT",
    "inventory": {
      "wood": 0,
      "stone": 0,
      "metal": 0,
      "energy": 0
    }
  },
  "resources": {
    "wood": 0,
    "stone": 0,
    "metal": 0,
    "energy": 0
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "commands": [
    {
      "action": "MOVE",
      "target_x": 1,
      "target_y": 0,
      "resources": {"wood": 0, "stone": 0, "metal": 0, "energy": 0}
    },
    {
      "action": "HARVEST",
      "resource_gained": "wood",
      "amount": 1,
      "resources": {"wood": 1, "stone": 0, "metal": 0, "energy": 0}
    }
  ],
  "final_state": {
    "grid": [
      [
        {"type": "EMPTY", "id": "0-0"},
        {"type": "EMPTY", "id": "1-0"}
      ]
    ],
    "bot": {
      "x": 1,
      "y": 0,
      "direction": "RIGHT",
      "inventory": {
        "wood": 1,
        "stone": 0,
        "metal": 0,
        "energy": 0
      }
    },
    "resources": {
      "wood": 1,
      "stone": 0,
      "metal": 0,
      "energy": 0
    },
    "population": 0
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Compilation error: line 2: undefined_variable"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "error": "Execution error: timeout"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/simulation/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "script": "bot.move()\nbot.harvest()",
    "grid": [[{"type": "EMPTY", "id": "0-0"}, {"type": "TREE", "id": "1-0"}]],
    "bot": {"x": 0, "y": 0, "direction": "RIGHT", "inventory": {"wood": 0, "stone": 0, "metal": 0, "energy": 0}},
    "resources": {"wood": 0, "stone": 0, "metal": 0, "energy": 0}
  }'
```

#### Save Game State

Save the current game state to the database.

**Endpoint:** `POST /simulation/save`

**Authentication:** Required

**Request Body:**
```json
{
  "grid_json": "[[...]]",
  "wood_count": 5,
  "stone_count": 3,
  "metal_count": 0,
  "energy_count": 0,
  "population_count": 1,
  "bot_x": 5,
  "bot_y": 3,
  "bot_direction": "RIGHT"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user_uuid",
  "grid_json": "[[...]]",
  "wood_count": 5,
  "stone_count": 3,
  "metal_count": 0,
  "energy_count": 0,
  "population_count": 1,
  "bot_x": 5,
  "bot_y": 3,
  "bot_direction": "RIGHT"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/simulation/save \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "grid_json": "[[...]]",
    "wood_count": 5,
    "stone_count": 3,
    "metal_count": 0,
    "energy_count": 0,
    "population_count": 1,
    "bot_x": 5,
    "bot_y": 3,
    "bot_direction": "RIGHT"
  }'
```

#### Get Saved Game State

Retrieve the user's saved game state.

**Endpoint:** `GET /simulation/save`

**Authentication:** Required

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user_uuid",
  "grid_json": "[[...]]",
  "wood_count": 5,
  "stone_count": 3,
  "metal_count": 0,
  "energy_count": 0,
  "population_count": 1,
  "bot_x": 5,
  "bot_y": 3,
  "bot_direction": "RIGHT"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "No save state found for this user"
}
```

**Example:**
```bash
curl http://localhost:5000/api/simulation/save \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Error Codes

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Error Response Format

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

### Common Errors

| Error | Description | Solution |
|-------|-------------|----------|
| `Token is missing` | Authorization header not provided | Include `Authorization: Bearer <token>` header |
| `Token is invalid` | Token is expired or malformed | Refresh token or login again |
| `Username already exists` | User registration with existing username | Choose a different username |
| `Invalid credentials` | Wrong username or password | Check credentials and try again |
| `Script is required` | Execute endpoint called without script | Include `script` field in request body |
| `Compilation error` | Script has syntax errors | Fix script syntax and try again |
| `Execution error: timeout` | Script exceeded 5-second limit | Optimize script or reduce iterations |
| `No save state found` | User has no saved game | Save a game state first |

## Rate Limiting

Currently, there are no rate limits implemented. Consider adding rate limiting for production use.

## CORS

The API supports CORS for cross-origin requests. All origins are currently allowed (`*`).

## Testing the API

### Using curl

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Login
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}' \
  | jq -r '.access_token')

# Get state
curl http://localhost:5000/api/simulation/state

# Execute script
curl -X POST http://localhost:5000/api/simulation/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"script": "bot.move()", "grid": [...], "bot": {...}, "resources": {...}}'
```

### Using JavaScript

```javascript
// Login
const response = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser',
    password: 'testpass'
  })
});
const { access_token } = await response.json();

// Execute script
const executeResponse = await fetch('http://localhost:5000/api/simulation/execute', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    script: 'bot.move()',
    grid: [...],
    bot: {...},
    resources: {...}
  })
});
const result = await executeResponse.json();
```
