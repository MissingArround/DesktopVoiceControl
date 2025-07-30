from pocketsphinx import LiveSpeech
import webbrowser  # Built-in module for opening websites

print("Listening... Say 'one' to open YouTube. Press Ctrl+C to stop.")

# Configure speech recognition
speech = LiveSpeech(
    lm=False,            # Better for single-word detection
    kws_threshold=1e-20,  # Sensitivity (lower = more sensitive)
    keyphrase="one",      # The trigger word
)

for phrase in speech:
    print("Heard:", phrase)
    if "one" in str(phrase).lower():  # check
        print(">>> Opening YouTube...")
        webbrowser.open("https://www.youtube.com")  # Opens in default browser
        break  # Stops listening after opening (remove if you want it to keep listening)