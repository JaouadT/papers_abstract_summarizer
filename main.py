from chatGPTPipleline import AbstractSummarizer
from papersRetriever import ArxivAPI
import time
import os
import pandas as pd
import argparse
import logging
from tqdm import tqdm

# Function to create an instance of the AbstractSummarizer class and set the prompt and API key with
def create_summarizer(prompt: str, api_key: str) -> AbstractSummarizer:
    prompt = prompt
    abstractSummarizer = AbstractSummarizer(prompt, api_key)
    return abstractSummarizer

# Function to create an instance of the ArxivAPI class and call the API to retrieve the paper information
def create_arxiv_api(query: str, start: int, max_results: int) -> ArxivAPI:
    query = query
    start = start
    max_results = max_results
    arxivAPI = ArxivAPI(query, start, max_results)
    return arxivAPI


def get_paper_information(paper_information: dict, summarizer: AbstractSummarizer) -> dict:
    # Loop over each paper in the dataframe and summarize the abstract using the AbstractSummarizer class
    for index, row in tqdm(paper_information.items()):
        try:
            summary = summarizer._summarise(row['abstract'])
        except Exception as e:
            raise Exception(f"Summarization failed for paper with index {index}, {e}")

        # add the summary to the dataframe in a new column called 'summary'
        paper_information[index]['summary'] = summary

        # Add a sleep timer to avoid overloading the API
        time.sleep(1)
    return paper_information

if __name__ == "__main__":

    # Create an instance of the ArgumentParser class
    parser = argparse.ArgumentParser(description='Process arguments for the main.py script')
    parser.add_argument('--prompt', type=str, help='The prompt to be used for the summarization', default="Summarize the following paper abstract and give the essential points for the novel method used in the minimum sentences possible.")
    parser.add_argument('--query', type=str, help='The query to be used for the Arxiv API call', default="breast ultrasound segmentation")
    parser.add_argument('--start', type=int, help='The starting index for the Arxiv API call', default=0)
    parser.add_argument('--max_results', type=int, help='The maximum number of results to return for the Arxiv API call', default=2)

    # Parse the arguments
    args = parser.parse_args()

    # Set the logging level to INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level = logging.INFO)

    # Set the arguments to variables
    prompt = args.prompt
    query = f"all:{args.query}"
    start = args.start
    max_results = args.max_results

    # Arguments
    logging.info(f"The prompt is set to: {prompt}")
    logging.info(f"The query is set to: {query}")
    logging.info(f"The start index is set to: {start}")
    logging.info(f"The maximum number of results is set to: {max_results}")


    # Read the API key from the openai_api_key.txt file
    with open(os.path.join("./openai_key", "openai_api_key.txt"), "r") as f:
        api_key = f.read()
    if not api_key:
        raise Exception("No API key found. Please add your API key to the openai_api_key.txt file")
    
    if len(api_key) < 51:
        raise Exception("The API key is too short. Please add your API key to the openai_api_key.txt file")

    # Create an instance of the AbstractSummarizer class
    summarizer = create_summarizer(prompt, api_key)

    # Create an instance of the ArxivAPI class
    arxiv_api = create_arxiv_api(query, start, max_results)

    logging.info("Calling the Arxiv API to retrieve the paper information ...")
    # Call the Arxiv API and retrieve the paper information
    paper_information = arxiv_api.get_paper_information()

    logging.info("Summarizing the paper abstract ...")
    # Create a dictionary of the paper information
    paper_information_dict = get_paper_information(paper_information, summarizer)

    # convert the dictionary to a dataframe
    paper_information_df = pd.DataFrame.from_dict(paper_information_dict, orient='index')

    # Save the dataframe to an excel file
    paper_information_df.to_excel("./output/paper_information.xlsx", index=False)

    logging.info("The paper information has been saved to paper_information.xlsx")
    logging.info("The script has finished running")

