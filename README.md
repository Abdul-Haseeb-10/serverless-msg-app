# 📬 CalabrioApp
This is a lightweight serverless Python application that accepts messages via an HTTP POST request, validates them, and stores them in an AWS DynamoDB table using an AWS Lambda function (Docker-based). It is exposed through an API Gateway.

---

## Project Structure
serverless-msg-app/
│
├── lambda_fn/                # Lambda function code (Dockerized)
│   ├── app.py
│   └── Dockerfile
│
├── serverless_msg_app/       # CDK stack definition
│   └── calabrio_app.py
│
├── tests/
│   ├── test_lambda.py
│   └── unit/
│       └── test_calabrio_app.py
│
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── cdk.json


## Features
- Accepts **POST** requests with JSON payload
- Validates message length and datetime format
- Stores messages in **DynamoDB**
- Lambda function packaged as a **Docker image**
- Infrastructure managed via **AWS CDK (Python)**
- **Unit tested** using `pytest`

---


## Deployment Instructions
> Make sure you have Docker Desktop running and AWS credentials configured (`aws configure`).

1. **Install Dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
2. **Bootstrap CDK (first time only)**
   ```bash
   cdk bootstrap
3. **Deploy the Stack**
    ```bash
   cdk deploy
4. **Get the API Gateway Endpoint**
   After deployment, you'll see output like: https://<api-id>.execute-api.<region>.amazonaws.com/prod/


## Testing the API
You can test the endpoint using tools like **Postman** or `curl`.
Note: The API Gateway base URL from the CDK deployment output **does not include** the `/submit` path.  
You **must** manually append `/submit` to the end of the base URL when sending requests.

 **Using Postman**

1. Set the method to `POST`
2. Enter the URL you got from the CDK output (e.g., `https://<api-id>.execute-api.<region>.amazonaws.com/prod/submit`)
3. Under **Headers**, add:  
   Content-Type: application/json
4. In the **Body** tab, select **raw** and choose **JSON** as the format. Paste the following sample payload:
   {
   "messageUUID": "123e4567-e89b-12d3-a456-426614174000",
   "messageText": "Hello from Calabrio!",
   "messageDatetime": "2025-06-21 12:00:00"
   }

You should receive a response with:

- statusCode: 200
- Body:
  {
  "message": "Saved successfully."
  }


## Running Unit Tests
This project includes unit tests using `pytest`.

 **To run the tests**

1. Activate your virtual environment:
   On Windows:
   ```
   .venv\Scripts\activate
   ```
   On Mac/Linux:
   ```
   source .venv/bin/activate
   ```

2. Run the tests using:

   ```
   python -m pytest
   ```
   
You should see output indicating test results. The tests cover:

- ✅ Successful message save with valid input
- ❌ Handling of invalid datetime formats
- ❌ Handling of too-short messages


## Troubleshooting

- Make sure Docker Desktop is running before deploying.
- If you see errors like `dockerDesktopLinuxEngine not found`, restart Docker or your machine.
- Ensure AWS credentials are set up via `aws configure`.
