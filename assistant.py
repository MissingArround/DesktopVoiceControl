import time
from model import model
from audio_utils import record_until_silence
from command_handler import COMMANDS, match_command, execute_command

def listen_and_respond():
    """Optimized main voice assistant loop"""
    print("\n🎤 Voice Assistant Activated")
    print("Available commands:")
    
    print("\n🌐 Websites:")
    for website, phrases in COMMANDS["website"].items():
        print(f"- {website.capitalize()}: {', '.join(phrases[:2])}")
    
    print("\n🚀 Applications:")
    for app, phrases in COMMANDS["application"].items():
        print(f"- {app.capitalize()}: {', '.join(phrases[:2])}")
    
    print("\n⚙️ System Commands:")
    for cmd, phrases in COMMANDS["system"].items():
        print(f"- {cmd.capitalize()}: {', '.join(phrases[:2])}")
    
    print("\nSay 'exit', 'quit', or 'stop' to terminate\n")
    
    try:
        while True:
            # Record audio
            audio_data = record_until_silence()
            
            if audio_data is None:
                print("No speech detected. Try again...")
                continue
            
            # Transcribe
            print("🔍 Processing...", end='', flush=True)
            start_time = time.time()
            result = model.transcribe(audio_data, language="en")
            transcript = result["text"].strip()
            proc_time = time.time() - start_time
            
            print(f" done in {proc_time:.1f}s")
            print(f"🎧 You said: {transcript}")
            
            if not transcript:
                print("⚠️ No speech recognized. Try again...")
                continue
                
            # Match and execute command
            command_info = match_command(transcript)
            if command_info:
                command_type, command = command_info
                should_exit = execute_command(command_type, command)
                if should_exit:
                    break
            else:
                print("⚠️ Command not recognized. Try:")
                print("  Websites: 'open youtube', 'search google'")
                print("  Apps: 'open notepad', 'open calculator'")
                print("  System: 'exit', 'shutdown computer'")
    
    except KeyboardInterrupt:
        print("\n🛑 Assistant stopped")