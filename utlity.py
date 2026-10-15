# pip intall google-genai
from google import genai

api_key ="AQ.Ab8RN6I70piWZXOMjeHHQtVEv79r67l34AF4SylEDqg7s_3fng"
# step1: authenticate

client =genai.Client(api_key=api_key)

prompt ="what is ai agent in simple words"

response=client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt
)

print(response.text)

