from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def call_llm(prompt, model=None, model_output_type=None, system_prompt=None):
    # Use model from environment variable or fall back to default
    model = model or os.environ.get("OPENAI_MODEL", "llama3.2")

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"),
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    if model_output_type:
        r = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=model_output_type,
        )
    else:
        r = client.chat.completions.create(model=model, messages=messages)

    result = r.choices[0].message
    if hasattr(result, "parsed"):
        return r.choices[0].message.parsed
    elif hasattr(result, "refusal") and result.refusal:
        print("Model refused to answer:", r.choices[0].message.refusal)
        return r.choices[0].message.refusal
    elif hasattr(result, "content"):
        return r.choices[0].message.content
    else:
        print("Unknown response format:", r)
