import google.generativeai as genai

# Set the API key
genai.configure(api_key="AIzaSyDeXoBZ13uiWoMzkvUzqA4ct48DaQJ_B4w")

def send_request(request):
    # Generate content
    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(request)
    return response.text
