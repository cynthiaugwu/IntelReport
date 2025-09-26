from anthropic import Anthropic
import os

print("API key loaded:", os.environ.get("ANTHROPIC_API_KEY", "NOT SET")[:10])

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

resp = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say hello world"}]
)

print(resp.content[0].text)
