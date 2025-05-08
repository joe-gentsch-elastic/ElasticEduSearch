import boto3
import json
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

"""
Script to call Claude 3 Sonnet on AWS Bedrock with a predefined prompt.
"""
# Load environment variables from .env file
load_dotenv()

def connect_to_aws():
    try:
        # Connect to AWS Bedrock
        bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    except Exception as e:
        print(f"An error occurred connecting to bedrock: {str(e)}")
    return bedrock_client

def invoke_model(user_prompt, context=None):
    bedrock_client = connect_to_aws()

    # Claude model settings
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    system_prompt = "You are Claude, a helpful AI assistant."
    max_tokens = 1000

    try:
        # Prepare the request body
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        })

        # Call the model
        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id
        )

        # Parse the response
        response_body = json.loads(response.get('body').read())

        # Print the response
        # print("\n--- Claude's Response ---")
        # print(response_body["content"][0]["text"])
        completion = response_body["content"][0]["text"]

    except ClientError as err:
        print(f"Error: {err.response['Error']['Message']}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return completion


#+------------------------------------------------------+
#|                   Main Execution                     |
#+------------------------------------------------------+
def execute_llm(user_prompt):
    #print(f'\nUser prompt: {user_prompt}')
    llm_answer = invoke_model(user_prompt)
    print(f'\nLLM Answer: {llm_answer}')
    return llm_answer

