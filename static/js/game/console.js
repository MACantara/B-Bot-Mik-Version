// Console output management

export function addConsoleOutput(message) {
    const console = document.getElementById('console');
    if (!console) return;
    
    const line = document.createElement('div');
    line.textContent = message;
    console.appendChild(line);
    console.scrollTop = console.scrollHeight;
}

export function clearConsole() {
    const console = document.getElementById('console');
    if (!console) return;
    
    console.innerHTML = '';
}
