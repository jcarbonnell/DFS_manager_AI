# An AI agent for managing decentralized file storage systems
from nearai.agents.environment import Environment

def run(env: Environment):
    # Your agent code here
    prompt = {"role": "system", "content": "You are a seasoned file manager agent, specialized in decentralized data storage architecture."}
    result = env.completion([prompt] + env.list_messages())
    env.add_reply(result)
    env.request_user_input()
    
run(env)

