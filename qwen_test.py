import base64
import requests

with open(r"<PATH_TO_IMAGE>", "rb") as f: # add your image path here
    b64 = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_API_KEY", # add your API key here
        "Content-Type": "application/json"
    },
    json={
        "model": "qwen/qwen2.5-vl-72b-instruct",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}, {"type": "text", "text": \
                """Extract from this prescription:
                - Drug name
                - Dose (gram, mg or units)
                - Frequency (times per day)
                - Treatment duration (e.g. "5 days", "1 week")
                - Special instructions or conditions (e.g. 'only if fever', 'take with food')
                - If a dosing schedule is written in the format:
                morning-noon-evening-night
                example: 0-1-1-0

                Return it as:
                {
                "morning": 0,
                "noon": 1,
                "evening": 1,
                "night": 0
                }

                Rules:
                - Do NOT infer schedules from frequency
                - If no explicit schedule exists, set "schedule" to null
                - If no duration is written, set "duration" to null
                - Return valid JSON only

                Schema:
                {
                "medications": [
                    {
                    "name": "",
                    "dose": "",
                    "frequency": "",
                    "duration": "",
                    "schedule": {
                    "morning": 0,
                    "noon": 0,
                    "evening": 0,
                    "night": 0
                    },
                    "notes": ""
                    }
                ]
                }
                """}
            ]
        }]
    }
)

print(response.json()["choices"][0]["message"]["content"])