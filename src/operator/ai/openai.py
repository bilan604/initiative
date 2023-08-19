import openai


def askGPT3(key, query):

    if len(query) == 0:
        return "Empty Query Recieved"

    openai.api_key = key
    try:
        curr_temp = 0.32
        response = openai.Completion.create(model="text-davinci-003",
                                            prompt=query,
                                            temperature=curr_temp,
                                            max_tokens=1400)
        message = response.choices[0].text
        return message
    except Exception as e:
        print("Error on OpenAI API Call:", e)
        return ""
    
def askGPT4(key, query):
    openai.api_key = key
    message=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": query}]
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message,
            temperature=0.5,
            max_tokens=1200,
            frequency_penalty=0.0
        ).choices[0].message.content.strip()
    return response



