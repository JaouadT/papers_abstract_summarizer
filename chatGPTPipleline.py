import openai
from typing import Optional

class AbstractSummarizer:
    """
    Class to summarize an abstract using the chatGPT API.
    :param prompt: str, the prompt to be used for the API call
    :param model: str, the model, default is 'gpt-3.5-turbo'
    :param temperature: int, the temperature, default is 1
    """
    def __init__(self, prompt: str, openai_key: str, model='gpt-3.5-turbo', temperature=1):
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        openai.api_key = openai_key

    def _summarise(self, abstract: str) -> Optional[str]:
        """
        Function to call the chatGPT API and return a the abstract prompt.
        :param abstract: str, the abstract to be sammarized
        :return: str, the response from the API call, or None if no response
        """

        # create a dict of parameters for the ChatCompletion API
        completion_params = {
            'model': self.model,
            'messages': [{"role": "system", "content": self.prompt},
                         {"role": "user", "content": abstract}],
            'temperature': self.temperature}

        # send a request to the ChatCompletion API and store the response
        response = openai.ChatCompletion.create(**completion_params)
        # extract the response content from the response object, if it exists
        if 'choices' in response and len(response.choices) > 0:
            response_content = response.choices[0]['message']['content']
        else:
            response_content = "chatGPT API call failed"

        return response_content