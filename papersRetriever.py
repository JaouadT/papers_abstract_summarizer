import pandas as pd
import requests
from typing import Optional
from bs4 import BeautifulSoup as bs
    
# Create a class to call the Arxiv API and extract the paper information
class ArxivAPI:
    """
    Class to call the Arxiv API and extract the paper information
    :param query: str, the query to be used for the API call
    :param start: int, the starting index for the API call
    :param max_results: int, the maximum number of results to return
    """
    def __init__(self, query: str, start: int, max_results: int):
        self.query = query
        self.start = start
        self.max_results = max_results

    def _get_text(self, soup, field: str, multiple_children = False) -> str:
        """Extracts text from a BeautifulSoup field"""
        try:
            if multiple_children:
                return("; ".join([author.text.strip().replace("\n", "") for author in soup.findAll(field)]))
            else:
                return soup.find(field).text.strip().replace("\n", " ")
        except:
            return("")

    def _get_response(self) -> Optional[str]:
        """
        Function to call the Arxiv API and return a the abstract prompt.
        :return: str, the response from the API call, or None if no response
        """
        # create a dict of parameters for the Arxiv API
        api_params = {
            'search_query': self.query,
            'start': self.start,
            'max_results': self.max_results}

        # send a request to the Arxiv API and store the response
        response = requests.get("http://export.arxiv.org/api/query", params=api_params)

        # extract the response content from the response object, if it exists
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Arxiv API call failed with status code {response.status_code}, {response.text}")

    def _parse_response(self, response: str) -> Optional[pd.DataFrame]:
        """
        Function to parse the response from the Arxiv API and return a dataframe.
        :param response: str, the response from the API call
        :return: pd.DataFrame, the parsed response
        """    
        # parse the response using BeautifulSoup
        soup = bs(response, 'xml')

        # Loop over each entry in the response and extract the relevant information
        # Store the information in a list of dictionaries
        paper_information = {}
        paper_index = 0
        for entry in soup.findAll('entry'):
            paper_id = self._get_text(entry, 'id')
            paper_title = self._get_text(entry, 'title')
            paper_abstract = self._get_text(entry, 'summary')
            paper_authors = self._get_text(entry, 'name', multiple_children=True)
            publication_date = self._get_text(entry, 'published')

            paper_information[paper_index] = {'id': paper_id,
                                      'title': paper_title,
                                      'abstract': paper_abstract,
                                      'authors': paper_authors,
                                      'publication_date': publication_date}
            paper_index += 1
            
        return paper_information
    
    def get_paper_information(self) -> Optional[pd.DataFrame]:
        """
        Function to call the Arxiv API and return a dataframe of paper information.
        :return: pd.DataFrame, the dataframe of paper information
        """
        if self.start < 0:
            raise ValueError("Start must be greater than or equal to 0.")
        if self.max_results < 2:
            raise ValueError("Max results must be greater than or equal to 2.")
        
        # call the API and store the response
        response = self._get_response()

        # if there is a response, parse it and return the dataframe
        if response:
            return self._parse_response(response)
        else:
            return None
        
        
        
