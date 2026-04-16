import librosa
import numpy as np
import warnings

# Suppress minor librosa warnings for cleaner output
warnings.filterwarnings('ignore')

class AudioForensicsExtractor:
    def __init__(self, sample_rate=16000, duration=10.0):
        self.sr = sample_rate
        self.duration = duration
        self.n_fft = 2048
        self.hop_length = 512

    def load_audio(self, file_path):
        """Loads and standardizes the audio input."""
        try:
            y, sr = librosa.load(file_path, sr=self.sr, duration=self.duration)
            return y
        except Exception as e:
            print(f"Error loading audio {file_path}: {e}")
            return None

    def extract_mel_spectrogram(self, y):
        """Generates the Mel-spectrogram for visual CNN analysis."""
        S = librosa.feature.melspectrogram(
            y=y, 
            sr=self.sr, 
            n_fft=self.n_fft, 
            hop_length=self.hop_length, 
            n_mels=128
        )
        S_dB = librosa.power_to_db(S, ref=np.max)
        return S_dB

    def extract_acoustic_features(self, y):
        """Extracts MFCCs and Spectral Contrast for baseline RF analysis."""
        mfccs = librosa.feature.mfcc(
            y=y, 
            sr=self.sr, 
            n_mfcc=20, 
            hop_length=self.hop_length
        )
        
        contrast = librosa.feature.spectral_contrast(
            y=y, 
            sr=self.sr, 
            n_fft=self.n_fft, 
            hop_length=self.hop_length
        )
        
        return mfccs, contrast