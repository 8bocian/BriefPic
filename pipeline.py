import math

from openaiapi import getKey, gpt3Completion
from dotenv import load_dotenv
# from transformers import GPT2Tokenizer


load_dotenv()
class Pipeline:

    def __init__(self):
        self.kernel_size = 40
        # print(os.getenv("TESSERACT_PATH"))
        # ts.pytesseract.tesseract_cmd =  os.getenv("TESSERACT_PATH")

        # self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

        getKey()
    def summary(self, text, prefix):

        # tokens = self.countTokens(text)
        # batches = math.ceil(tokens/2040)
        # textPartLen = math.ceil(len(text)/batches)
        # textPartStart = 0
        # summary = ""

        # for i in range(batches):
        #     if (i-1 != batches):
        #         textPartEnd  = text[textPartLen*i:textPartLen*(i+1)].find('.')
        #         textPart = text[textPartStart:textPartEnd]
        #         textPartStart = textPartEnd
        #     else:
        #         textPart = text[textPartStart:]
        #     fullQuery = f"{prefix} {textPart}"
        #     print(fullQuery)
        #     summary += gpt3Completion(fullQuery) + " "
        fullQuery = f"{prefix} {text}"

        summary = gpt3Completion(fullQuery)
        return summary

    # def countTokens(self, text):
    #     return len(self.tokenizer(text)['input_ids'])
