# papers_abstract_summarizer

Summarize the latest research papers abstract from Arxiv using chatGPT for staying up to date about the latest state of the art papers. 
This project was built because of a personal need, which is to stay up to date about the latest research papers in the field I am working on.

## Features
- Using a query, retrieve a desired number of latest papers from `Arxiv.com`.
- Using ChatGPT, summarize the abstarct of the papers.
- Save the papers information:
    - Paper id;
    - Paper title;
    - Paper abstrat;
    - Paper authors;
    - Paper publication date;
    - Paper summary.

## Requirements

1. Python: Python 3.8 or newer.
2. GPT-3.5 API Access.


## How to Use
1. Clone the repository: 'https://github.com/JaouadT/papers_abstract_summarizer.git'.
2. cd into the repository: `cd papers_abstract_summarizer`.
3. Install requirements: `pip install -r requirements.txt`.
4. Save your GPT-3.5 API key in a file named `openai_api_key.txt` in the folder `openai_key`.
3. Run the script `main.py` with the desired query and number of papers to summarize. For example: `python main.py --query "Ultrasound images segmentation" --max_results 5`.

Note: 
1. The script will save the papers information in an excel spreadsheet named `paper_information.xlsx` in the folder `output`.
2. The script expects to retrieve at least two papers to summarize. If the number of papers retrieved is less than two, the script will raise an error.

## Contributing
If you have any suggestions on how to improve the code, please feel free to open an issue or a pull request.
Many features can be added to this project, such as:
- Support multiple open access papers sources (e.g. IEEE, Springer, ...).
- Summarize a paper from its url.
- Summarize a paper from its id.
- Summarize the papers introduction and conclusion.
- Summarize the papers body.
- Extract the papers keywords.
- Extract the papers references.
- Build a web app for the project.
- ...

