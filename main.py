import numpy as np
from model import model
from audio_utils import SAMPLE_RATE
from assistant import listen_and_respond

if __name__ == "__main__":
    # Warm up the model for faster first response
    print("⚙️ Initializing... (warming up model)")
    warm_up_audio = np.zeros(int(SAMPLE_RATE * 0.1), dtype=np.float32)
    model.transcribe(warm_up_audio, language="en")
    
    listen_and_respond()