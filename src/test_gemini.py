from google import genai

client = genai.Client(api_key="AIzaSyAzQKmGfvChTEOa2hKwR98l6WCcY2FDuaI")

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Explain what a research paper is."
)

print(response.text)