import json
import boto3
import botocore.config
from datetime import datetime

def blog_generate_using_bedrock(blogTopic:str)-> str:
    prompt = f"""
    <s>[INST] Human: Write a 200 words blog on the topic {blogTopic}
    Assistant:[/INST]
    """
    
    body = {
        "prompt": prompt,
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.9
    }
    
    try:
        bedrock= boto3.client('bedrock-runtime',region_name='us-east-1',config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3}))
        
        response= bedrock.invoke_model(body=json.dumps(body),modelId="meta.llama3-70b-instruct-v1:0")
        
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        blog_details = response_data.get('generation')
        
        return blog_details
    
    except Exception as e:
        print(f"[ERROR] There is an error during Inference: {e}")
        return ""

def save_to_s3_bucket(s3_key,s3_bucket, generate_blog):
    s3 = boto3.client('s3')
    
    try: 
        s3.put_object(Bucket=s3_bucket, Key= s3_key, Body= generate_blog)
    except Exception as e:
        print(f"[ERROR] Caused error while uploading to s3 bucket: {e}")


def lambda_handler(event,context):
    
    event = json.loads(event['body'])
    blog_topic = event['blog_topic']
    
    generateblog = blog_generate_using_bedrock(blog_topic)
    
    if generateblog:
        currtime = datetime.now().strftime('%H%M%S')
        s3_key = f"blog_output/{currtime}.txt"
        s3_bucket = 'aws-bedrock-12'
        save_to_s3_bucket(s3_key,s3_bucket,generateblog)
        
    else:
        print('no blog is created')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Generated Blog Uploaded')
    }


if __name__ == "__main__":
    # This simulates the 'event' object that AWS Lambda receives from API Gateway.
    # The 'body' is a JSON formatted STRING.
    test_event = {
        "body": json.dumps({
            "blog_topic": "The future of space exploration with AI"
        })
    }
    
    # The second argument to the handler, 'context', is not used in this script, so we can pass None.
    result = lambda_handler(test_event, None)
    print(result)