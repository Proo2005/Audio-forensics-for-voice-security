import unittest
import numpy as np
import sys
import os

# Add src to path so we can import the extractor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from extractor import AudioForensicsExtractor

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = AudioForensicsExtractor(duration=2.0)
        # Create 2 seconds of dummy white noise data instead of loading a real file
        self.dummy_audio = np.random.randn(self.extractor.sr * 2)

    def test_spectrogram_shape(self):
        S_dB = self.extractor.extract_mel_spectrogram(self.dummy_audio)
        # Verify 128 mel bands are generated
        self.assertEqual(S_dB.shape[0], 128)

    def test_acoustic_features(self):
        mfccs, contrast = self.extractor.extract_acoustic_features(self.dummy_audio)
        # Verify 20 MFCCs and 7 contrast bands are generated
        self.assertEqual(mfccs.shape[0], 20)
        self.assertEqual(contrast.shape[0], 7)

if __name__ == '__main__':
    unittest.main()