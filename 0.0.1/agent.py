# An AI agent for managing decentralized file storage systems
from nearai.agents.environment import Environment
from ipfshttpclient import Client

ipfs_client = Client('/dns/localhost/tcp/5001/http')

def run(env: Environment):
    # System role definition for the agent
    system_prompt = {"role": "system", "content": "You are a Decentralized File Storage Manager AI Agent, specialized in managing decentralized file storage systems, particularly with IPFS. You handle analysis, tagging, indexing, organization, optimization, and ensure privacy and security."}
    
    # Retrieve all messages in the conversation
    messages = env.list_messages()

    # Check for user commands or queries
    if messages:
        last_message = messages[-1]
        user_message = last_message['content'].lower()
    
        if user_message.startswith('!addfile'):
            try:
                file_path = user_message.split(' ', 2)[2]
                response = ipfs_client.add(file_path)
                cid = response['Hash']
                env.write_file(f"{cid}.info", f"Added file: {file_path}")
                env.add_reply(f"File added successfully with CID: {cid}")
            except Exception as e:
                env.add_reply(f"Error adding file: {str(e)}")

    # Request for more user input
    env.request_user_input()

run(env)