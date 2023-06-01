import openai
from typing import Optional


prompt = "Summarize the following paper abstract and give the essential points for the novel method used in the minimum sentences possible."
abstract = """U-Net and its extensions have achieved great success in medical image segmentation. However, due to the inherent local characteristics of ordinary convolution operations, U-Net encoder cannot effectively extract global context information. In addition, simple skip connections cannot capture salient features. In this work, we propose a fully convolutional segmentation network (CMU-Net) which incorporates hybrid convolutions and multi-scale attention gate. The ConvMixer module extracts global context information by mixing features at distant spatial locations. Moreover, the multi-scale attention gate emphasizes valuable features and achieves efficient skip connections. We evaluate the proposed method using both breast ultrasound datasets and a thyroid ultrasound image dataset; and CMU-Net achieves average Intersection over Union (IoU) values of 73.27% and 84.75%, and F1 scores of 84.81% and 91.71%."""

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