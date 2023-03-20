import os
import openai
from dotenv import load_dotenv

from utils import createLogger

load_dotenv()

def getKey():
    try:
        key = os.getenv("API_KEY")
        openai.api_key = key
        return "success"
    except Exception as e:
        return f"failure, {e}"


def gpt3Completion(prompt, engine='text-davinci-003', temp=0.7,
                   top_p=1.0, tokens=4000, freq_pen=0.0, pres_pen=0.0,
                   stop=('USER:', 'TIM:')):
    logger = createLogger()

    max_retry = 5
    retry = 0
    # prompt = prompt.encode(encoding="ASCII", errors="ignore").decode()
    while retry < max_retry:
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                    messages=[{"role": "system", "content": prompt}])
            type = 0
        except:
            response = openai.Completion.create(engine=engine, prompt=prompt,
                                                temperature=temp,
                                                top_p=top_p, frequency_penalty=freq_pen,
                                                presence_penalty=pres_pen, stop=stop)
            type = 1
        try:
            if type == 0:
                text = response['choices'][0]['message']['content'].strip()
            elif type == 1:
                text = response['choices'][0]['text'].strip()
            else:
                raise Exception
            logger.info(type)
            logger.info(text[:100])
            return text
        except Exception as e:
            retry += 1
            logger.info(len(prompt))
            print(len(prompt))
            logger.info(e)
            logger.info(response)
            return e


if __name__ == '__main__':
    prompt = 'Summarize the text'
    result = gpt3Completion(prompt)
    print(result)
