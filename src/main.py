from open_ai.client import OpenaiClient
from settings import settings

token = settings.get("OPENAI_TOKEN")
client = OpenaiClient(token)

image = client.generate_image("Sunray cat mainkun")
