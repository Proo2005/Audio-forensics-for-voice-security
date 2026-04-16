import json
import base64
import os
import tempfile
import joblib
import numpy as np
from src.extractor import AudioForensicsExtractor

# 1. Cold Start Optimization: Load artifacts globally so they persist between warm invocations
print("Loading Forensics Model and Extractor into memory...")
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/voice_forensics_model.pkl')
forensics_model = joblib.load(MODEL_PATH)
extractor = AudioForensicsExtractor()

def lambda_handler(event, context):
    """
    AWS Lambda entry point. Expects a JSON payload:
    { "audio_base64": "<base64_encoded_wav_string>" }
    """
    try:
        # 2. Parse the incoming JSON payload from API Gateway
        body = json.loads(event.get('body', '{}'))
        audio_b64 = body.get('audio_base64')
        
        if not audio_b64:
            return format_response(400, {"error": "Missing audio_base64 payload."})

        # 3. Decode audio and write to Lambda's ephemeral storage (/tmp/)
        audio_bytes = base64.b64decode(audio_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name

        # 4. Execute Phase 1: Digital Signal Processing
        y = extractor.load_audio(tmp_path)
        if y is None:
            return format_response(422, {"error": "Invalid audio format. Must be readable by soundfile."})
            
        mfccs, contrast = extractor.extract_acoustic_features(y)
        feature_vector = np.hstack((np.mean(mfccs, axis=1), np.mean(contrast, axis=1)))
        
        # Reshape for a single prediction: (1, 27)
        feature_vector = feature_vector.reshape(1, -1)

        # 5. Execute Phase 2: Machine Learning Inference
        prediction = forensics_model.predict(feature_vector)[0]
        probabilities = forensics_model.predict_proba(feature_vector)[0]
        
        # prediction: 0 = Authentic, 1 = Synthetic
        is_high_risk = bool(prediction == 1)
        confidence_score = round(float(probabilities[prediction]) * 100, 2)

        # Clean up ephemeral storage
        os.remove(tmp_path)

        # 6. Return standard security telemetry
        telemetry = {
            "status": "success",
            "analysis": {
                "high_risk_synthetic_artifacts_detected": is_high_risk,
                "confidence_score": confidence_score,
                "latency_optimized": True
            }
        }
        return format_response(200, telemetry)

    except Exception as e:
        return format_response(500, {"error": f"Internal processing error: {str(e)}"})

def format_response(status_code, body):
    """Formats the output strictly for AWS API Gateway integration."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*" # Enables CORS for frontend dashboards
        },
        "body": json.dumps(body)
    }