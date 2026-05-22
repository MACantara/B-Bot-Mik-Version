from flask import Blueprint, request, jsonify
from core.database import supabase
from core.security import decode_token
from core.script_interpreter import ScriptInterpreter, ScriptValidationError, simulate_execution
from functools import wraps

simulation_bp = Blueprint('simulation', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = decode_token(token)
        if payload is None:
            return jsonify({'error': 'Token is invalid'}), 401
        
        request.user_id = payload.get('user_id')
        request.username = payload.get('sub')
        return f(*args, **kwargs)
    return decorated


@simulation_bp.route('/state', methods=['GET'])
def get_simulation_state():
    """Returns the demo 20x20 grid configuration"""
    # Create a demo 20x20 grid with various tile types
    demo_grid = []
    for y in range(20):
        row = []
        for x in range(20):
            # Distribute trees and rocks across the larger grid
            if (x, y) in [(2, 3), (5, 7), (8, 2), (1, 8), (6, 4), (12, 15), (15, 5), (18, 12), (3, 17), (10, 10)]:
                cell = {"type": "TREE", "id": f"{x}-{y}"}
            elif (x, y) in [(3, 1), (7, 5), (4, 8), (9, 3), (2, 6), (14, 11), (16, 8), (11, 14), (5, 18), (13, 2)]:
                cell = {"type": "ROCK", "id": f"{x}-{y}"}
            elif (x, y) in [(4, 4), (5, 4), (6, 4), (7, 4), (8, 4)]:  # Sample road
                cell = {"type": "ROAD", "id": f"{x}-{y}"}
            else:
                cell = {"type": "EMPTY", "id": f"{x}-{y}"}
            row.append(cell)
        demo_grid.append(row)
    
    bot_state = {
        "x": 0,
        "y": 0,
        "direction": "RIGHT",
        "inventory": {"wood": 0, "stone": 0, "metal": 0, "energy": 0}
    }
    
    return jsonify({
        "grid": demo_grid,
        "bot": bot_state,
        "population": 0,
        "resources": {"wood": 0, "stone": 0, "metal": 0, "energy": 0}
    })


@simulation_bp.route('/save', methods=['POST'])
@token_required
def save_simulation_state():
    """Persists the player's layout progress and resource tallies"""
    data = request.get_json()
    user_id = request.user_id
    
    # Check if user already has a save state
    response = supabase.table("save_states").select("*").eq("user_id", user_id).execute()
    
    save_state_data = {
        "user_id": user_id,
        "grid_json": data.get('grid_json'),
        "wood_count": data.get('wood_count', 0),
        "stone_count": data.get('stone_count', 0),
        "metal_count": data.get('metal_count', 0),
        "energy_count": data.get('energy_count', 0),
        "population_count": data.get('population_count', 0),
        "bot_x": data.get('bot_x', 0),
        "bot_y": data.get('bot_y', 0),
        "bot_direction": data.get('bot_direction', 'RIGHT')
    }
    
    if response.data:
        # Update existing save
        result = supabase.table("save_states").update(save_state_data).eq("id", response.data[0]["id"]).execute()
        return jsonify(result.data[0])
    else:
        # Create new save
        result = supabase.table("save_states").insert(save_state_data).execute()
        return jsonify(result.data[0])


@simulation_bp.route('/save', methods=['GET'])
@token_required
def get_saved_state():
    """Retrieves the user's saved simulation state"""
    user_id = request.user_id
    response = supabase.table("save_states").select("*").eq("user_id", user_id).execute()
    if not response.data:
        return jsonify({'error': 'No save state found for this user'}), 404
    return jsonify(response.data[0])


@simulation_bp.route('/execute', methods=['POST'])
@token_required
def execute_script():
    """
    Execute a user-submitted script using the AST-based interpreter.
    Returns a command queue for frontend animation and the final game state.
    """
    data = request.get_json()
    script = data.get('script', '')
    initial_grid = data.get('grid', [])
    initial_bot = data.get('bot', {'x': 0, 'y': 0, 'direction': 'RIGHT', 'inventory': {'wood': 0, 'stone': 0, 'metal': 0, 'energy': 0}})
    initial_resources = data.get('resources', {'wood': 0, 'stone': 0, 'metal': 0, 'energy': 0})
    
    if not script:
        return jsonify({'error': 'Script is required'}), 400
    
    try:
        # Parse and validate the script using AST interpreter
        interpreter = ScriptInterpreter()
        command_queue = interpreter.parse_and_validate(script)
        
        # Simulate execution to generate detailed command queue
        detailed_queue, final_grid, final_resources, final_population, final_bot = simulate_execution(
            command_queue,
            initial_grid,
            initial_bot,
            initial_resources
        )
        
        return jsonify({
            'success': True,
            'commands': detailed_queue,
            'final_state': {
                'grid': final_grid,
                'bot': final_bot,
                'resources': final_resources,
                'population': final_population
            }
        })
    
    except ScriptValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Execution error: {str(e)}'}), 500
