import os
import shutil
from __init__ import create_app

def clear_cache():
    """Clear Python cache and temporary files"""
    cache_dirs = [
        '__pycache__',
        '.pytest_cache',
        '.mypy_cache',
    ]
    
    for cache_dir in cache_dirs:
        for root, dirs, files in os.walk('.', topdown=True):
            if cache_dir in dirs:
                cache_path = os.path.join(root, cache_dir)
                try:
                    shutil.rmtree(cache_path)
                    print(f'Cleared cache: {cache_path}')
                except Exception as e:
                    print(f'Failed to clear {cache_path}: {e}')
                dirs.remove(cache_dir)
    
    # Clear .pyc files
    for root, dirs, files in os.walk('.', topdown=True):
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f'Removed: {file_path}')
                except Exception as e:
                    print(f'Failed to remove {file_path}: {e}')

app = create_app()

if __name__ == '__main__':
    print('Clearing cache...')
    clear_cache()
    print('Starting server...')
    app.run(host='0.0.0.0', port=5000, debug=True)
