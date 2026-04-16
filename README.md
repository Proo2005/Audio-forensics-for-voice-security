
# Audio Forensics For Voice Security
## 1. ENVIRONMENT INITIALIZATION
## Installation

Install my-project with npm

```bash
python -m venv forensics_env
source forensics_env/bin/activate  # On Windows: forensics_env\\Scripts\\activate
pip install -r requirements.txt
pip install pytest
```

    
## 2. Validating the Extractor
```
pytest tests/test_extractor.py
```
## 3. Model Training
```
cd src
python classifier.py
```
Upon successful training, the system will output accuracy metrics and export the compiled weights to models/voice_forensics_model.pkl.

## 4. Cloud Deployment (Docker & AWS)

#### 1.From the root directory containing the Dockerfile:
```
docker build -t audio-forensics-api .
```
#### 2. Push to AWS Elastic Container Registry (ECR)
```
aws ecr get-login-password --region YOUR_REGION | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com
docker tag audio-forensics-api:latest YOUR_ACCOUNT_ID.dkr.ecr.YOUR_[REGION.amazonaws.com/audio-forensics-api:latest](https://REGION.amazonaws.com/audio-forensics-api:latest)
docker push YOUR_ACCOUNT_ID.dkr.ecr.YOUR_[REGION.amazonaws.com/audio-forensics-api:latest](https://REGION.amazonaws.com/audio-forensics-api:latest)
```
#### 3. Configure AWS Serverless Infrastructure
```
Create a new AWS Lambda function using the uploaded Container Image.

Adjust Lambda settings: Set Memory to 2048 MB and Timeout to 15 seconds.

Create an HTTP API via API Gateway and route a POST method to your Lambda function.
```
## 5.Usage & API Integration
EndPoints Requests
```
{
  "audio_base64": "<base64_encoded_wav_string>"
}
```


EndPoint Responce
```
{
    "status": "success",
    "analysis": {
        "high_risk_synthetic_artifacts_detected": true,
        "confidence_score": 98.45,
        "latency_optimized": true
    }
}
```
You can utilize the test_api.py script provided in the repository to read a local .wav file, encode it, and transmit it securely to your local Docker container or live AWS API Gateway URL.

# Disclaimer
```
This project is intended for educational and defensive security purposes. Datasets containing synthetic speech must be handled responsibly and in accordance with local biometric privacy laws.
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("README.md created successfully.")

```