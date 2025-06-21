FROM public.ecr.aws/lambda/python:3.11

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Install boto3 (just in case)
RUN pip install boto3

# Set the entry point
CMD ["app.handler"]
