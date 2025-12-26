from openai import OpenAI

client = OpenAI()

def generate_ad_copy(platform, context):
    prompt = f"Create {platform} ad copy using this research: {context}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content