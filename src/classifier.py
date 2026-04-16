import numpy as np
import os
import glob
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
from extractor import AudioForensicsExtractor 

class ForensicsClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            class_weight='balanced'
        )
        self.extractor = AudioForensicsExtractor() 

    def engineer_features(self, file_path):
        """Processes an audio file and flattens its acoustic features into a 1D vector."""
        y = self.extractor.load_audio(file_path)
        if y is None: 
            return None
            
        mfccs, contrast = self.extractor.extract_acoustic_features(y)
        
        # Average the features over time to create a single 27-dimensional vector 
        # (20 MFCC means + 7 Spectral Contrast means)
        feature_vector = np.hstack((np.mean(mfccs, axis=1), np.mean(contrast, axis=1)))
        return feature_vector

    def build_dataset(self, real_audio_dir, fake_audio_dir):
        """Iterates through directories to build the X (features) and y (labels) arrays."""
        X = []
        y_labels = []

        print("Processing Authentic Audio...")
        for file in glob.glob(os.path.join(real_audio_dir, '*.wav')):
            features = self.engineer_features(file)
            if features is not None:
                X.append(features)
                y_labels.append(0) # 0 = Real

        print("Processing Synthetic Audio...")
        for file in glob.glob(os.path.join(fake_audio_dir, '*.wav')):
            features = self.engineer_features(file)
            if features is not None:
                X.append(features)
                y_labels.append(1) # 1 = Fake

        return np.array(X), np.array(y_labels)

    def train_and_export(self, real_dir, fake_dir, export_path="../models/voice_forensics_model.pkl"):
        """Trains the model and saves it to the models directory."""
        X, y = self.build_dataset(real_dir, fake_dir)
        
        if len(X) == 0:
            print("Error: No valid audio files processed. Check directory paths.")
            return

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("Training Random Forest Classifier...")
        self.model.fit(X_train, y_train)

        print("\nEvaluating Model Accuracy...")
        predictions = self.model.predict(X_test)
        
        print(f"Overall Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")
        print(classification_report(y_test, predictions, target_names=['Authentic (0)', 'Synthetic (1)']))

        # Ensure the models directory exists
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        joblib.dump(self.model, export_path)
        print(f"Model successfully exported to {export_path}")

if __name__ == "__main__":
    # Update these paths to point to your downloaded datasets
    REAL_DIR = "../data/authentic_speech/"
    FAKE_DIR = "../data/synthetic_speech/"
    
    classifier = ForensicsClassifier()
    classifier.train_and_export(REAL_DIR, FAKE_DIR)