FROM public.ecr.aws/lambda/python:3.11
COPY app.py ${LAMBDA_TASK_ROOT}
RUN pip install boto3
CMD ["app.handler"]