# Use the official AWS Lambda Python 3.10 base image
FROM public.ecr.aws/lambda/python:3.10

# Install system dependencies required by librosa and soundfile
RUN yum update -y && \
    yum install -y libsndfile && \
    yum clean all

# Copy dependency manifest and install Python libraries
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy the core application files and models into the container
COPY src/ ${LAMBDA_TASK_ROOT}/src/
COPY models/ ${LAMBDA_TASK_ROOT}/models/
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to point to the handler function inside app.py
CMD [ "app.lambda_handler" ]