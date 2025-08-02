import whisper

# Optimized model loading - using 'small.en' for best speed/accuracy balance
model = whisper.load_model("small.en")