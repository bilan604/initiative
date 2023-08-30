import time
import openai


# function name is depreciated
def get_openai_result(prompt):
    if type(prompt) != str:
        return
    if len(prompt) == 0:
        return "Empty Query Recieved"

    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=1800)
    return response.choices[0].text.strip()


def get_gpt_3_5_result(prompt, model_version="gpt-3.5-turbo-16k"):
    message=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
                model=model_version,
                messages=message,
                temperature=0.5,
                max_tokens=1000,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
        return response
    except Exception as e:
        if isinstance(e, openai.error.RateLimitError):
            print("Sleeping for 60 seconds")
            time.sleep(60)
            response = openai.ChatCompletion.create(
                model=model_version,
                messages=message,
                temperature=0.5,
                max_tokens=1000,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
            return response
        return None


def get_gpt4_result(prompt, model_version="gpt-4"):

    message=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
                model=model_version,
                messages=message,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
        return response
    except Exception as e:
        print("Error:", e)
        if isinstance(e, openai.error.RateLimitError):
            print("Sleeping for 60 seconds")
            time.sleep(60)
            response = openai.ChatCompletion.create(
                model=model_version,
                messages=message,
                temperature=0.5,
                max_tokens=1000,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
            return response
        return None

def prompt_gpt_3_5_turbo(prompt):
    message=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
        return response
    except Exception as e:
        print("Error:", e)
        if isinstance(e, openai.error.RateLimitError):
            print("Sleeping for 60 seconds")
            time.sleep(60)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=0.5,
                max_tokens=1000,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
            return response
        return None











