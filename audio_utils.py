import sounddevice as sd
import numpy as np
import time

# Audio parameters - optimized for performance
SAMPLE_RATE = 16000
CHUNK_SIZE = 2048
MIN_SPEECH_DURATION = 0.1
MAX_RECORDING_DURATION = 4.0

# Precompute constants for efficiency
SILENCE_DURATION = 1.0
SILENCE_FRAMES = int(SILENCE_DURATION * SAMPLE_RATE / CHUNK_SIZE)
MAX_FRAMES = int(MAX_RECORDING_DURATION * SAMPLE_RATE / CHUNK_SIZE)

# Global calibration to run once
SILENCE_THRESHOLD = None

def calibrate_silence_threshold(duration=1.5):
    """Calibrate silence threshold once at startup"""
    global SILENCE_THRESHOLD
    if SILENCE_THRESHOLD is not None:
        return SILENCE_THRESHOLD
        
    print("Calibrating ambient noise... (Please stay silent)")
    calibration = sd.rec(int(duration * SAMPLE_RATE), 
                         samplerate=SAMPLE_RATE, 
                         channels=1, 
                         dtype='float32')
    sd.wait()
    rms = np.sqrt(np.mean(calibration**2))
    SILENCE_THRESHOLD = max(rms * 2.0, 0.01)
    print(f"Calibrated silence threshold: {SILENCE_THRESHOLD:.4f}")
    return SILENCE_THRESHOLD

def record_until_silence():
    """Optimized audio recording with efficient buffer handling"""
    print("\n🎤 Listening... (Say a command or press Ctrl+C to stop)")
    recording = []
    silent_frames = 0
    speech_start = None
    speech_detected = False
    
    # Pre-calibrated threshold
    threshold = calibrate_silence_threshold()
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, 
                        dtype='float32', blocksize=CHUNK_SIZE) as stream:
        start_time = time.time()
        
        while True:
            # Check for timeout
            if time.time() - start_time > MAX_RECORDING_DURATION:
                break
            
            # Read audio chunk
            chunk, _ = stream.read(CHUNK_SIZE)
            chunk = np.squeeze(chunk)
            
            # Efficient RMS calculation
            rms = np.sqrt(np.mean(chunk**2))
            
            if rms > threshold:
                if not speech_detected:
                    speech_start = time.time()
                    print("Voice detected...", end='', flush=True)
                speech_detected = True
                silent_frames = 0
            elif speech_detected:
                silent_frames += 1
                if silent_frames >= SILENCE_FRAMES:
                    break
            
            # Only store audio after speech is detected
            if speech_detected:
                recording.append(chunk)
            
            # Stop if we've exceeded max frames
            if len(recording) >= MAX_FRAMES:
                break
    
    if speech_detected:
        audio = np.concatenate(recording)
        duration = time.time() - speech_start
        print(f" captured {duration:.1f}s")
        return audio
    return None