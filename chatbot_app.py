from openai import OpenAI

client = OpenAI(api_key="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")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
