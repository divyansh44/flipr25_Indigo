# News Aggregation and Summarization Project

## Overview
This project fetches news articles across various topics from a specific city and state (e.g., Delhi) and processes them to generate a structured and comprehensive news article. The steps involved in this process include:
1. Fetching news articles based on the specified location and topic.
2. Filtering out duplicate and redundant news articles.
3. Fetching additional articles related to the unique news articles.
4. Summarizing each news topic by combining information from multiple sources.
5. Classifying the summarized news articles into categories.
6. Storing and merging the final structured news articles for reuse and further publishing.

## Installation and Setup
### Prerequisites
Ensure you have the following installed:
- Python (>= 3.8)
- Miniconda or Anaconda (recommended)
- Required Python packages (listed below)

### Clone the Repository
```bash
git clone <your-repository-url>
cd <repository-directory>
```

### Create a Virtual Environment
Using Conda (Recommended):
```bash
conda create --name news_env python=3.8 -y
conda activate news_env
```

Using venv:
```bash
python -m venv news_env
source news_env/bin/activate   # On macOS/Linux
news_env\Scripts\activate      # On Windows
```

### Install Dependencies
Run the following command to install the necessary Python libraries:
```bash
pip install -r requirements.txt
```

### Configuration
Update the `configs.yaml` file with the required parameters:
```yaml
topic: "Technology"
location: "Delhi, India"
```
Also, update the API keys in your script:
```python
gemini_api_key = "your-gemini-api-key"
serp_api_key = "your-serp-api-key"
```

## Running the Project
To fetch, process, summarize, and classify news articles, run:
```bash
python main.py
```
This script will:
1. Fetch news articles based on the location and topic.
2. Process and summarize them.
3. Classify them into categories.
4. Store the processed articles in `News.json`.

### Merging New News Data
To merge newly fetched news with the existing dataset, run:
```bash
python -c "from your_script import merge_and_save_news; merge_and_save_news()"
```
This will ensure that duplicate articles are removed and all structured news articles are updated.

## File Structure
```
project-root/
│-- SRC/
│   ├── Summary_Generator.py
│   ├── Prompts.py
│   ├── Helper_func.py
│-- configs.yaml
│-- requirements.txt
│-- main.py
│-- News.json
│-- New_News.json
│-- README.md
```

## Expected Output
The final processed news articles will be stored in `News.json` in the following format:
```json
[
    {
        "text": "Summarized news content...",
        "category": "Technology"
    },
    {
        "text": "Another summarized news...",
        "category": "Politics"
    }
]
```

## Notes
- If you encounter an error related to `IProgress not found`, update Jupyter and ipywidgets:
```bash
pip install --upgrade jupyter ipywidgets
```
- Ensure API keys are valid and have sufficient quota.

## Future Improvements
- Adding more news sources for better summarization.
- Improving classification accuracy with advanced NLP techniques.
- Enhancing duplicate filtering with better similarity metrics.

## Contributing
If you'd like to contribute, feel free to fork the repository and submit a pull request!

## License
This project is open-source and available under the MIT License.

