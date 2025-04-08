# RUN " python llm_access/test_groq_report.py " IN THE CONSOLE WITH THE BELOW SECTION UNCOMMENTED TO TEST GROQ FUNCTIONALITY
# BE SURE TO COMMENT OUT " from DjangoApp import settings " BEFORE TESTING THE SCRIPT
# import os
# import sys
# import django
# from pathlib import Path
# from dotenv import load_dotenv
# BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(str(BASE_DIR))  # Ensure Python can find 'DjangoApp'
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoApp.settings")
#
# load_dotenv()
#
# django.setup()
#
# from django.conf import settings

##################################

import httpx
from DjangoApp import settings


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_groq_response_async(prompt):
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 5000,
        }

        response = await client.post(GROQ_API_URL, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.json()}"