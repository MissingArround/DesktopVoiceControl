import webbrowser
import os
import subprocess
from difflib import get_close_matches

# Enhanced command dictionary with application support
COMMANDS = {
    "website": {
        "youtube": ["youtube", "open youtube", "go to youtube", "watch videos", "tube", "you tube"],
        "google": ["google", "open google", "search google", "web search", "search the web", "look up"],
        "github": ["github", "open github", "go to github", "code repository", "git hub", "my code"],
    },
    "application": {
        "notepad": ["notepad", "open notepad", "text editor"],
        "calculator": ["calculator", "open calculator"],
        "paint": ["paint", "mspaint", "open paint", "drawing app", "draw"],
        "explorer": ["file explorer", "open files", "browse files", "file manager", "explorer"],
    },
    "system": {
        "exit": ["exit", "quit", "stop", "goodbye", "shutdown", "do stop"],
        "shutdown": ["shutdown computer", "turn off computer", "power off", "turn off pc"],
        "restart": ["restart computer", "reboot computer"]
    }
}

# Map applications to their executable paths
APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
}

def match_command(transcript):
    """Optimized command matching with priority handling"""
    transcript = transcript.lower().strip()
    
    # First check for system commands (highest priority)
    for command, phrases in COMMANDS["system"].items():
        for phrase in phrases:
            if phrase in transcript:
                return ("system", command)
    
    # Check website commands
    for website, phrases in COMMANDS["website"].items():
        for phrase in phrases:
            if phrase in transcript:
                return ("website", website)
    
    # Check application commands
    for app, phrases in COMMANDS["application"].items():
        for phrase in phrases:
            if phrase in transcript:
                return ("application", app)
    
    # Then try fuzzy match for all phrases
    all_phrases = []
    for category in COMMANDS:
        for command in COMMANDS[category]:
            all_phrases.extend(COMMANDS[category][command])
    
    matches = get_close_matches(transcript, all_phrases, n=1, cutoff=0.5)
    
    if matches:
        matched_phrase = matches[0]
        # Find which command the matched phrase belongs to
        for category in COMMANDS:
            for command, phrases in COMMANDS[category].items():
                if matched_phrase in phrases:
                    return (category, command)
    
    return None

def execute_command(command_type, command):
    """Execute commands based on their type"""
    if command_type == "system":
        if command == "exit":
            print("👋 Goodbye!")
            return True  # Signal to exit
        elif command == "shutdown":
            print("🛑 Shutting down computer...")
            os.system("shutdown /s /t 1")
            return True
        elif command == "restart":
            print("🔄 Restarting computer...")
            os.system("shutdown /r /t 1")
            return True
            
    elif command_type == "website":
        print(f"🌐 Opening {command}...")
        webbrowser.open(f"https://{command}.com")
        
    elif command_type == "application":
        if command in APP_PATHS:
            print(f"🚀 Launching {command}...")
            try:
                # Try to open using the default system method
                os.startfile(APP_PATHS[command])
            except AttributeError:
                # For non-Windows systems, use subprocess
                subprocess.Popen([APP_PATHS[command]])
        else:
            print(f"⚠️ Application '{command}' not configured")
    
    return False