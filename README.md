# Blog Generator using AWS Bedrock (API Gateway + Lambda + S3)

This project is a serverless blog generation application built using AWS Bedrock, API Gateway, AWS Lambda, and Amazon S3.
It exposes a REST API that accepts a blog topic, generates a blog using a foundation model hosted on Bedrock, and stores the generated content in an S3 bucket.

## Overview

The application workflow is:

- A client sends a blog topic via API Gateway
- API Gateway triggers an AWS Lambda function
- Lambda invokes a Bedrock foundation model (Meta LLaMA 3 – 70B Instruct)
- The model generates a ~200-word blog
- The generated blog is saved to Amazon S3
- A success response is returned to the client

This project was built as a learning PoC to understand how LLMs can be integrated into serverless AWS architectures.

## Architecture

- API Gateway – Exposes the REST endpoint
- AWS Lambda – Handles request processing and orchestration
- AWS Bedrock Runtime – Generates blog content using LLaMA 3
- Amazon S3 – Stores generated blog outputs

## Code Flow

- API Gateway receives a POST request with the blog topic
- Lambda handler parses the request body
- Bedrock Runtime is invoked using boto3
- Generated text is written to an S3 bucket
- Lambda returns a response back through API Gateway

### Input Format

The API expects a JSON payload:
```bash
{
  "blog_topic": "The future of space exploration with AI"
}
```

### Output

A text file is created in the S3 bucket under:
```bash
blog_output/<timestamp>.txt
```

The API returns a success response:

```bash
{
  "statusCode": 200,
  "body": "Generated Blog Uploaded"
}
```

### AWS Services Used

- AWS Bedrock – Foundation model inference
- Amazon API Gateway – REST API endpoint
- AWS Lambda – Serverless compute
- Amazon S3 – Object storage
- boto3 – AWS SDK for Python

### Prerequisites

- AWS account with access to AWS Bedrock
- API Gateway REST API connected to Lambda
- IAM role for Lambda with permissions:
   - `bedrock:InvokeModel`
   - `s3:PutObject`
- Python 3.9 or above
- Existing S3 bucket

### Local Testing

The script includes a __main__ block to simulate a Lambda event locally:
```bash
test_event = {
    "body": json.dumps({
        "blog_topic": "The future of space exploration with AI"
    })
}
```

### Notes

- This project focuses on Bedrock inference and service integration
- Basic error handling is included for simplicity
- Model ID and region can be updated as needed

### Future Enhancements

- Add input validation at API Gateway level
- Add authentication (API keys / IAM / Cognito)
- Improve logging and monitoring
- Make blog length and style configurable
- Store metadata along with generated content
