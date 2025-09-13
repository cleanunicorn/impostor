from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def call_llm(prompt, model=None, model_output_type=None):
    # Use model from environment variable or fall back to default
    model = model or os.environ.get("OPENAI_MODEL", "llama3.2")

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"),
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )

    if model_output_type:
        r = client.beta.chat.completions.parse(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format=model_output_type,
        )
    else:
        r = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )

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
