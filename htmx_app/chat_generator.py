# Streamed response emulator
def response_generator(user_message: str):
    # In a real scenario we would want to pass the user message to an LLM
    response = "Hello there! How can I assist you today?" * int(1000 / 8) # 10,000 characters

    for word in response.split():
        yield word + " "