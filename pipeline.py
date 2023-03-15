from openaiapi import getKey, gpt3Completion
from dotenv import load_dotenv

load_dotenv()
class Pipeline:

    def __init__(self):
        self.kernel_size = 40
        # print(os.getenv("TESSERACT_PATH"))
        # ts.pytesseract.tesseract_cmd =  os.getenv("TESSERACT_PATH")
        getKey()
    def summary(self, text, prefix):

        summary = gpt3Completion(f"{prefix} {text}")


        return summary
