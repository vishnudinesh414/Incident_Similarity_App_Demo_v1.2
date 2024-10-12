import pandas as pd
import spacy
import numpy as np
import umap.umap_ as umap
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from nltk.corpus import stopwords
from nltk import download
import re
import joblib

# Download necessary NLTK data only if not already downloaded
download('stopwords', quiet=True)

class ClusteringModel:
    def __init__(self):
        self.kmeans_model = None
        self.scaler = None
        self.umap_reducer = None
        self.sentence_model = None
        self.cluster_assignments = None  # To store cluster assignments
        self.df = None  # To store the DataFrame with descriptions

    def remove_before_colon(self, sentence):
        # Remove content before the first colon or "DVT:"
        sentence = sentence.split("DVT:", 1)[-1] if "DVT:" in sentence else sentence.split(":", 1)[-1]
        
        # Define patterns to remove specific terms/versions
        patterns = [
            r'\balizon(?:_?[a-zA-Z]?\d+)?\b',
            r'\bv\d{5}\b',
            r'\bv\d+\.\d+\.\d+(?:\.\d+)?\b'
        ]
        
        for pattern in patterns:
            sentence = re.sub(pattern, '', sentence)

        return sentence.strip()

    def preprocess_data(self, file_path):
        df = pd.read_csv(file_path, encoding='latin1').dropna(subset=["Short Description"])
        df.reset_index(drop=True, inplace=True)
        nlp = spacy.load("en_core_web_sm")
        
        # Clean and tokenize descriptions in one go using a single apply function
        df["Cleaned_Description"] = (
            df["Short Description"]
            .apply(self.remove_before_colon)
            .str.lower()
            .str.strip()
            .str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
            .apply(lambda x: [token.text for token in nlp(x)])
            .apply(lambda x: [word for word in x if word not in self.get_stopwords()])
            .apply(lambda x: [token.lemma_ for token in nlp(' '.join(x))])
            .apply(lambda x: ' '.join(x))
        )

        return df

    def get_stopwords(self):
        stop_words = set(stopwords.words('english'))
        additional_stopwords = {'issue', 'poco', 'corvette14', 'corvette', 'pocowestern', 'error', 'problem', 
                                'zbook', 'western', 'probook', 'notebook', 'elitebook', 'elitedesk', 
                                'dragonfly', 'pavilion', 'zbookfury'}
        stop_words.update(additional_stopwords)
        return stop_words 

    def train(self, file_path, n_clusters=92):
        self.df = self.preprocess_data(file_path)
        
        cleaned_descriptions = self.df["Cleaned_Description"].tolist()
    
        self.sentence_model = SentenceTransformer('all-MiniLM-L12-v2')
        embeddings = self.sentence_model.encode(cleaned_descriptions, convert_to_tensor=True)
    
        self.scaler = StandardScaler()
        scaled_embeddings = self.scaler.fit_transform(embeddings.cpu().numpy())
    
        self.umap_reducer = umap.UMAP(
            n_components=2,
            n_neighbors=15,
            min_dist=0.1,
            metric='cosine',
            random_state=42
        )
        
        reduced_embeddings = self.umap_reducer.fit_transform(scaled_embeddings)
    
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=46)
        self.cluster_assignments = self.kmeans_model.fit_predict(reduced_embeddings)
    
        # Save cluster assignments to a CSV file
        self.df['Cluster'] = self.cluster_assignments
        self.df.to_csv('../data/cluster_assignments.csv', index=False)
        
        cluster_centers_df = pd.DataFrame(self.kmeans_model.cluster_centers_)
        cluster_centers_df.to_csv("../data/cluster_centers.csv", index=False)

    def save(self, filename):
        joblib.dump({
            'kmeans_model': self.kmeans_model,
            'scaler': self.scaler,
            'umap_reducer': self.umap_reducer,
            'cluster_assignments': self.cluster_assignments,
            'sentence_model': self.sentence_model,
            'df': self.df,
        }, filename)

    @classmethod
    def load(cls, filename):
        return joblib.load(filename)


if __name__ == "__main__":
    model = ClusteringModel()
    model.train('../data/new_pseudonymized_in.csv')
    model.save('../models/K-Mean_MiniLM-Custom_Incident_Classification_Model.pkl')