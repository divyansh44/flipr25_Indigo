# import torch
# from transformers import BertModel, BertTokenizer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np
# import google.generativeai as genai

# class NewsFilter:
#     def __init__(self,threshold=0.8):
#         # Load pre-trained BERT model and tokenizer
#         model_name = 'bert-base-uncased'
#         self.tokenizer = BertTokenizer.from_pretrained(model_name)
#         self.model = BertModel.from_pretrained(model_name)
#         self.model.eval()  # Set model to evaluation mode
        
#         self.threshold = threshold
#         # self.unique_texts = []


#     # Function to get BERT embeddings
#     def get_bert_embedding(self, text):
        
#         inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=256)
#         with torch.no_grad():
#             outputs = self.model(**inputs)
#         # Get the mean of the last hidden state
#         last_hidden_state = outputs.last_hidden_state.squeeze(0)
#         embedding = torch.mean(last_hidden_state, dim=0)
#         return embedding.numpy()

#     # Function to filter unique news descriptions
#     def filter_unique_texts(self,texts):
        
#         unique_embeddings = []
#         news_indices = []
#         for index, text in enumerate(texts):
#             current_embedding = self.get_bert_embedding(text)

#             # Compare with all previously accepted unique texts
#             is_unique = True
#             for emb in unique_embeddings:
#                 similarity = cosine_similarity(current_embedding.reshape(1, -1), emb.reshape(1, -1))[0][0]
#                 if similarity >= self.threshold:
#                     is_unique = False
#                     break

#             # Accept the text only if it's unique compared to all previously accepted texts
#             if is_unique:
#                 # self.unique_texts.append(text)
#                 unique_embeddings.append(current_embedding)
#                 news_indices.append(index)
            
#             # Stop if 6 unique texts are found
#             if len(news_indices) == 6:
#                 break
        
#         return news_indices
        
#     def filter_similar_texts(self,texts):
#         unique_embeddings = []
#         news_indices = []
#         for index, text in enumerate(texts):
#             current_embedding = self.get_bert_embedding(text)

#             # Compare with all previously accepted unique texts
#             is_similar = True
#             for emb in unique_embeddings:
#                 similarity = cosine_similarity(current_embedding.reshape(1, -1), emb.reshape(1, -1))[0][0]
#                 if similarity <= self.threshold:
#                     is_similar = False
#                     break

#             # Accept the text only if it's unique compared to all previously accepted texts
#             if is_similar:
#                 # self.unique_texts.append(text)
#                 unique_embeddings.append(current_embedding)
#                 news_indices.append(index)
            
#             # Stop if 4 similar texts are found
#             if len(news_indices) == 4:
#                 break
        
#         return news_indices

# class News_Authenticator():
#     def __init__(self , gemini_api_key, merge_prompt):
#         # self.merge_prompt=merge_prompt
#         genai.configure(api_key=gemini_api_key)
#         self.model =  genai.GenerativeModel(
#                 model_name="gemini-1.5-pro",
#                 # system_instruction=merge_prompt
#             )
#         self.system_prompt=merge_prompt
        
#     def merge_text(self, summaries):
#             """
#             Merges multiple pre-existing summaries using Gemini.
            
#             Parameters:
#                 summaries (list): List of summary texts to merge
#                 merge_prompt (str, optional): Custom system instruction for merging
            
#             Returns:
#                 str: The merged summary
            
#             Raises:
#                 ValueError: If empty list is provided
#             """
#             if not summaries:
#                 raise ValueError("At least one summary must be provided")

#             merge_input=""
#             for i, summary in enumerate(summaries, 1):
#                 merge_input += f"Summary {i}:\n{summary}\n\n"
#             prompt = f"{self.system_prompt}\n\nHere are the summaries to merge\n\n{merge_input}"
#             # Merge the summaries
#             merged_response = self.model.generate_content(prompt)
#             return merged_response.text if merged_response.text else "Merging failed"

# # First, run this cell to install required packages
# # !pip install transformers torch pandas seaborn matplotlib

# # Then run this cell for the imports and classifier code
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from transformers import pipeline
# from IPython.display import display, HTML

# class NewsClassifier:
#     def __init__(self):
#         # Load pre-trained zero-shot classification pipeline
#         self.classifier = pipeline("zero-shot-classification",
#                                  model="facebook/bart-large-mnli")
        
#         # Define our target categories
#         self.categories = [
#             "Sports",
#             "Finance",
#             "Crimes",
#             "Entertainment",
#             "Political",
#             "Technology",
#             "Others"
#         ]
    
#     def classify_text(self, text):
#         """
#         Classify a single piece of text into one of our categories
#         """
#         result = self.classifier(
#             text,
#             candidate_labels=self.categories,
#             hypothesis_template="This text is about {}."
#         )
        
#         # Get all categories and scores
#         return {
#             'scores': dict(zip(result['labels'], result['scores']))
#         }
    
#     def classify_multiple(self, texts):
#         """
#         Classify multiple texts and return results as a DataFrame
#         """
#         results = []
#         for text in texts:
#             classification = self.classify_text(text)
#             best_category = max(classification['scores'].items(), key=lambda x: x[1])
            
#             results.append({
#                 'category': best_category[0],
#                 'content': text,
#                 'confidence': round(best_category[1], 3),
#                 'all_scores': classification['scores']
#             })
        
#         return pd.DataFrame(results)
    
#     def plot_results(self, results_df):
#         """
#         Create visualizations for the classification results
#         """
#         # Category distribution
#         plt.figure(figsize=(12, 5))
#         sns.countplot(data=results_df, x='category')
#         plt.title('Distribution of Categories')
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.show()
        
#         # Confidence scores
#         plt.figure(figsize=(12, 5))
#         sns.boxplot(data=results_df, x='category', y='confidence')
#         plt.title('Confidence Scores by Category')
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.show()


import torch
from transformers import BertModel, BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import google.generativeai as genai

class NewsFilter:
    def __init__(self,threshold=0.8):
        # Load pre-trained BERT model and tokenizer
        model_name = 'bert-base-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()  # Set model to evaluation mode
        
        self.threshold = threshold
        # self.unique_texts = []


    # Function to get BERT embeddings
    def get_bert_embedding(self, text):
        
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=256)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Get the mean of the last hidden state
        last_hidden_state = outputs.last_hidden_state.squeeze(0)
        embedding = torch.mean(last_hidden_state, dim=0)
        return embedding.numpy()

    # Function to filter unique news descriptions
    def filter_unique_texts(self,texts):
        
        unique_embeddings = []
        news_indices = []
        for index, text in enumerate(texts):
            current_embedding = self.get_bert_embedding(text)

            # Compare with all previously accepted unique texts
            is_unique = True
            for emb in unique_embeddings:
                similarity = cosine_similarity(current_embedding.reshape(1, -1), emb.reshape(1, -1))[0][0]
                if similarity >= self.threshold:
                    is_unique = False
                    break

            # Accept the text only if it's unique compared to all previously accepted texts
            if is_unique:
                # self.unique_texts.append(text)
                unique_embeddings.append(current_embedding)
                news_indices.append(index)
            
            # Stop if 6 unique texts are found
            if len(news_indices) == 6:
                break
        
        return news_indices
        
    def filter_similar_texts(self,texts):
        unique_embeddings = []
        news_indices = []
        for index, text in enumerate(texts):
            current_embedding = self.get_bert_embedding(text)

            # Compare with all previously accepted unique texts
            is_similar = True
            for emb in unique_embeddings:
                similarity = cosine_similarity(current_embedding.reshape(1, -1), emb.reshape(1, -1))[0][0]
                if similarity <= self.threshold:
                    is_similar = False
                    break

            # Accept the text only if it's unique compared to all previously accepted texts
            if is_similar:
                # self.unique_texts.append(text)
                unique_embeddings.append(current_embedding)
                news_indices.append(index)
            
            # Stop if 4 similar texts are found
            if len(news_indices) == 4:
                break
        
        return news_indices

class News_Authenticator():
    def __init__(self , gemini_api_key, merge_prompt):
        # self.merge_prompt=merge_prompt
        genai.configure(api_key=gemini_api_key)
        self.model =  genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                # system_instruction=merge_prompt
            )
        self.system_prompt=merge_prompt
        
    def merge_text(self, summaries):
            """
            Merges multiple pre-existing summaries using Gemini.
            
            Parameters:
                summaries (list): List of summary texts to merge
                merge_prompt (str, optional): Custom system instruction for merging
            
            Returns:
                str: The merged summary
            
            Raises:
                ValueError: If empty list is provided
            """
            if not summaries:
                raise ValueError("At least one summary must be provided")

            merge_input=""
            for i, summary in enumerate(summaries, 1):
                merge_input += f"Summary {i}:\n{summary}\n\n"
            prompt = f"{self.system_prompt}\n\nHere are the summaries to merge\n\n{merge_input}"
            # Merge the summaries
            merged_response = self.model.generate_content(prompt)
            return merged_response.text if merged_response.text else "Merging failed"

# First, run this cell to install required packages
# !pip install transformers torch pandas seaborn matplotlib

# Then run this cell for the imports and classifier code
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from transformers import pipeline
from IPython.display import display, HTML

class NewsClassifier:
    def __init__(self):
        # Load pre-trained zero-shot classification pipeline
        self.classifier = pipeline("zero-shot-classification",
                                 model="facebook/bart-large-mnli")
        
        # Define our target categories
        self.categories = [
            "Sports",
            "Finance",
            "Crimes",
            "Entertainment",
            "Political",
            "Technology",
            "Others"
        ]
    
    def classify_text(self, text):
        """
        Classify a single piece of text into one of our categories
        """
        result = self.classifier(
            text,
            candidate_labels=self.categories,
            hypothesis_template="This text is about {}."
        )
        
        # Get all categories and scores
        return {
            'scores': dict(zip(result['labels'], result['scores']))
        }
    
    def classify_multiple(self, texts):
        """
        Classify multiple texts and return results as a DataFrame
        """
        results = []
        for text in texts:
            classification = self.classify_text(text)
            best_category = max(classification['scores'].items(), key=lambda x: x[1])
            
            results.append({
                'category': best_category[0],
                'content': text,
                'confidence': round(best_category[1], 3),
                'all_scores': classification['scores']
            })
        
        return pd.DataFrame(results)
    
    def plot_results(self, results_df):
        """
        Create visualizations for the classification results
        """
        # Category distribution
        plt.figure(figsize=(12, 5))
        sns.countplot(data=results_df, x='category')
        plt.title('Distribution of Categories')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        # Confidence scores
        plt.figure(figsize=(12, 5))
        sns.boxplot(data=results_df, x='category', y='confidence')
        plt.title('Confidence Scores by Category')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()



import requests
import os
import IPython.display as display
from PIL import Image
from io import BytesIO
import base64
class ImgBBUploader:
    def __init__(self, api_key=None):
        self.api_key = api_key or "YOUR_API_KEY"  # Replace with your API key
        self.upload_url = "https://api.imgbb.com/1/upload"

    def encode_image(self, image_path):
        """Convert image to base64"""
        with open(image_path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')

    def upload_image(self, image_path):
        """Upload image to ImgBB and return the URLs"""
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError("Image file not found!")

            # Prepare the image
            image_base64 = self.encode_image(image_path)

            # Prepare the payload
            payload = {
                "key": self.api_key,
                "image": image_base64,
                "name": os.path.basename(image_path)
            }

            # Make the request
            response = requests.post(self.upload_url, payload)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Extract URLs from response
            data = response.json()
            if data["success"]:
                return {
                    "direct_url": data["data"]["url"],
                    "delete_url": data["data"]["delete_url"],
                    "thumbnail_url": data["data"]["thumb"]["url"],
                    "medium_url": data["data"].get("medium", {}).get("url"),
                }
            else:
                raise Exception("Upload failed: " + str(data))

        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {str(e)}")
            return None
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None