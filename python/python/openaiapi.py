import os
import openai

def getKey():
    try:
        key = open("C:/Users/Bocian/Desktop/openaiapikey.txt").readlines()[0]
        openai.api_key = key
        return "success"
    except Exception as e:
        pass
    try:
        key = os.getenv("API_KEY")
        openai.api_key = key
        return "success"
    except Exception as e:
        return f"failure, {e}"


def gpt3Completion(prompt, engine='text-davinci-002', temp=0.7,
                   top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0,
                   stop=('USER:', 'TIM:')):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding="ASCII", errors="ignore").decode()

    while retry < max_retry:
        try:
            response = openai.Completion.create(engine=engine, prompt=prompt,
                                                temperature=temp, max_tokens=tokens,
                                                top_p=top_p, frequency_penalty=freq_pen,
                                                presence_penalty=pres_pen, stop=stop)
            text = response['choices'][0]['text'].strip()

            return text
        except Exception as e:
            retry += 1
            return e

if __name__ == '__main__':
    prompt = 'Summarize the text'
    result = gpt3Completion(prompt)
    print(result)
