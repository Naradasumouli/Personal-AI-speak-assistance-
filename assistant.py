import ollama

print("Mama Bro Started")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye Bro")
        break

    response = ollama.chat(
        model="qwen2.5-coder:3b",
        messages=[
            {
                "role": "system",
                "content": """
                You are Mama Bro, a professional AI assistant.
                Speak clearly, concisely and helpfully.
                You are friendly and intelligent.
                """
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("Mama Bro:", response["message"]["content"])