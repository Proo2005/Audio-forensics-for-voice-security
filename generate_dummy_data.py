# generate_dummy_data.py
import numpy as np
import soundfile as sf
import os

def create_dummy_wav(directory, prefix, count=10):
    os.makedirs(directory, exist_ok=True)
    sr = 16000
    for i in range(count):
        # Generate 2 seconds of random audio noise
        audio_data = np.random.uniform(-1, 1, sr * 2) 
        sf.write(f"{directory}/{prefix}_{i}.wav", audio_data, sr)

print("Synthesizing dummy audio files for pipeline validation...")
create_dummy_wav("data/authentic_speech", "real")
create_dummy_wav("data/synthetic_speech", "fake")
print("Data staging complete. Proceed to model training.")