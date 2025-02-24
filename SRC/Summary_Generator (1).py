import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from typing import List, Dict, Optional
import time
import re
import pandas as pd
from SRC.Helper_func import * 
from SRC.Prompts import system_prompt, merge_prompt

class NewsSearcher:
    def __init__(self, location: str,topic: str, serp_api_key: str):
        self.location = location
        self.topic = topic
        self.api_key = serp_api_key
        self.base_url = "https://serpapi.com/search.json"
        
    def search_news(self, query: str, num_results: int = 3) -> List[Dict]:
        """
        Search for news articles using SERP API.
        Returns list of dictionaries with title and url.
        """
        search_query = f"{self.location} {self.topic} {query}"
        
        try:
            params = {
                "api_key": self.api_key,
                "q": search_query,
                "tbm": "nws",
                "num": num_results
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            results = []
            if 'news_results' in data:
                for result in data['news_results'][:num_results]:
                    results.append({
                        'title': result['title'],
                        'url': result['link']
                    })
            # print(results)
            return results
            
        except Exception as e:
            print(f"Error in SERP API search: {str(e)}")
            return []

class ArticleScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_article(self, url):
        """
        Scrapes the given URL and returns the text content and a clean, concise description for Google search.
        Args:
            url (str): The webpage URL to scrape.
        Returns:
            dict: A dictionary containing the URL, its extracted text content, and a clean short description.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text_content = soup.get_text(separator="\n", strip=True)
            
            # Extract a concise description for Google search
            description = None
            meta_tags = [
                {'property': 'og:title'}, 
                {'name': 'twitter:title'},
                {'name': 'description'}, 
                {'property': 'og:description'},
                {'name': 'twitter:description'}
            ]
            
            for tag in meta_tags:
                meta = soup.find('meta', tag)
                if meta and meta.get('content'):
                    description = meta['content']
                    break
            
            # If no meta description is found, get the first 150 characters of the first paragraph
            if not description:
                paragraphs = soup.find_all('p')
                if paragraphs:
                    description = paragraphs[0].get_text()
            
            # Clean and format the description
            if description:
                # Remove encoded characters and unnecessary spaces
                description = description.encode('latin1', 'ignore').decode('utf-8', 'ignore')
                description = description.strip()
                
                # Remove everything after the first "|"
                description = re.split(r'\s*\|\s*', description)[0]
                
                # Limit the description to 150 characters for better search usability
                description = (description[:147] + '...') if len(description) > 150 else description
            
            return {
                "url": url,
                "content": text_content,
                "description": description if description else ""
            }

class ContentSummarizer:
    def __init__(self, system_prompt, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.system_prompt = system_prompt
    
    def summarize_article(self, article: str) -> str:
        """
        Summarize a single article using Gemini API.
        """
        prompt = f"{self.system_prompt}\n\nHere is the article to summarize:\n\n{article}"
        # print('reached here')
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error in summarization: {str(e)}")
            return None

class NewsAgent1:
    def __init__(self, system_prompt, topic: str, gemini_api_key: str, serp_api_key: str,location: str = "Delhi"):
        self.searcher = NewsSearcher(location,topic, serp_api_key)
        self.scraper = ArticleScraper()
        self.summarizer = ContentSummarizer(system_prompt,gemini_api_key)
        
    def process_news(self, num_links, initial_query: str = "" ) -> pd.DataFrame:
        """
        Process news articles and return a DataFrame with individual summaries
        """
        # Get news articles
        results = self.searcher.search_news(initial_query , num_links)
        # Create lists to store data
        data = []
        summary = None
        for result in results:
            # Scrape article
            article_text = self.scraper.scrape_article(result['url'])
            
            if article_text:
                # Store the data
                data.append({
                    'title': result['title'],
                    'url': result['url'],
                    'full_text': article_text
                })
            # Add delay to avoid rate limiting
            time.sleep(2)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        return df

class NewsAgent2:
    def __init__(self, merge_prompt,
                 system_prompt,
                 topic: str, 
                 gemini_api_key: str,
                 serp_api_key: str,
                 similarity_threshold=0.75
                 
                ):
        location=""
        self.searcher = NewsSearcher(location,topic, serp_api_key)
        self.scraper = ArticleScraper()
        # self.summarizer = ContentSummarizer(merge_prompt,gemini_api_key)
        self.authenticator = News_Authenticator(gemini_api_key , merge_prompt)
        self.newsfilter = NewsFilter(threshold=similarity_threshold)
        self.summary_generator = ContentSummarizer(system_prompt,api_key=gemini_api_key)
    def process_news(self, num_links, initial_query: str = "" ):
        """
        Process news articles and return a DataFrame with individual summaries
        """
        # Get news articles
        results = self.searcher.search_news(initial_query , num_links) ##num_links links on one description
                                                                        ##by SerpApi Call
        # Create lists to store data
        data = []
        summary = None
        for result in results: 
            # Scrape article
            article_text = self.scraper.scrape_article(result['url'])
            if article_text:
                data.append(article_text)
            # Add delay to avoid rate limiting
            time.sleep(2)
        # print(data)
        texts = []
        for i in data:
            texts.append(i['description']) 
        similar_texts_indices = self.newsfilter.filter_similar_texts(texts)
        # print(similar_texts_indices)
        similar_texts = []
        for i in similar_texts_indices:
            similar_texts.append(self.summary_generator.summarize_article(data[i]['content']))
        summary = self.authenticator.merge_text(similar_texts)
        
        # Create DataFrame
        
        return summary
