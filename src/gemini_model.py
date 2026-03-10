from google import genai

client = genai.Client(api_key="AIzaSyCp9Jh8uR5hZuZZe__E7kJBsL0QNnF_Jm0")

def generate_with_gemini(prompt):

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text