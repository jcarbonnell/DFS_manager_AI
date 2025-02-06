# An AI agent for managing decentralized file storage systems
from nearai.agents.environment import Environment
import json
import boto3
from mutagen import File

def extract_metadata(file_path):
    # Extract metadata from file
    audio = File(file_path)
    metadata = {
        'title': audio.get('title', ['Unknown'])[0],
        'artist': audio.get('artist', ['Unknown'])[0],
    }
    return metadata

def upload_to_s3(file_path, metadata, bucket_name):
    # Upload file to S3
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, f"{metadata['artist']}_{metadata['title']}.mp3")
    return f"https://{bucket_name}.s3.amazonaws.com/{metadata['artist']}_{metadata['title']}.mp3"

def run(env: Environment):
    # System prompt for context
    prompt = {"role": "system", "content": "You are a seasoned file manager agent, specialized in decentralized data storage architecture."}
    
    # request user input, where users drop files or provide file paths
    env.request_user_input()

    # assuming the user input is now part of the message list
    messages = env.list_messages()

    # Check if there's a new message from the user
    if messages and messages[-1]['role'] == 'user':
        user_input = messages[-1]['content']

        try:
            metadata = extract_metadata(user_input)

            # use AI for tagging, classifying, and more complex tasks

            # upload file to S3
            url = upload_to_s3(user_input, metadata, "1000fans-theosis")
            # add the result to the conversation
            env.add_reply(f"File processed and uploaded. URL: {url}. Metadata: {json.dumps(metadata)}")
        except Exception as e:
            # If there's an error (e.g., file not found), inform the user with more detailed guidance
            error_message = f"Error processing file: {str(e)}. Please ensure the file path is correct. Here's how you can proceed:\n- To upload a file, provide the full path like: /path/to/your/file.mp3\n- Type 'help' for more information on using this agent."
            env.add_reply(error_message)

        # continue the conversation with the AI
        result = env.completion([prompt] + messages)
        env.add_reply(result)

        # ask for moe input or end conversation
        env.request_user_input()

run(env)