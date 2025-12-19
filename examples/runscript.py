from qwsengine.scripting import ScriptExecutor, ExecutionContext
#from scripting.executor import ScriptExecutor, ExecutionContext
#from scripting import ScriptExecutor, ExecutionContext

# Create context with your browser window
context = ExecutionContext(
    browser_window=my_browser_window,
    settings_manager=my_settings_manager
)

# Create executor
executor = ScriptExecutor(context)

# Load from JSON
script_json = {
    "version": "1.0",
    "commands": [
        {"command": "load_url", "url": "https://codaland.com/ip.php"},
        {"command": "save_html", "filename": "page1.html", "path": "./output"},
        {"command": "pause", "seconds": 10},
        {"command": "load_url", "url": "https://codaland.com/ipcheck.php"},
        {"command": "save_html", "filename": "page2.html", "path": "./output"},
        {"command": "pause", "seconds": 10}
    ]
}

executor.load_from_json(script_json)

# Execute with progress callback
def on_progress(current, total, description):
    print(f"[{current+1}/{total}] {description}")

success = executor.execute(on_progress=on_progress)

# Check results
if success:
    print("Script executed successfully!")
else:
    print("Errors occurred:")
    for idx, cmd, error in executor.get_errors():
        print(f"  [{idx}] {cmd}: {error}")

# View logs
for log in context.get_logs():
    print(log)