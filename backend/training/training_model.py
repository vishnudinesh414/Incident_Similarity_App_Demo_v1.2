import pandas as pd
import umap.umap_ as umap
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from nltk import download
import joblib
import logging
from common.incident_preprocessor import IncidentPreProcessor
from store.json_handler import read_data, update_data

logging.basicConfig(level=logging.INFO, format='%(message)s')

preProcessingInstence = IncidentPreProcessor()
download('stopwords', quiet=True)

class ClusterTrainingingModel:
    def __init__(self):
        self.kmeans_model = None
        self.scaler = None
        self.umap_reducer = None
        self.sentence_model = None
        self.cluster_assignments = None
        self.df = None
        data = read_data('store/store.json')
        self.current_csv_length = data['current_length']
        self.n_cluster = data['n_clusters']
        
    def cluster_number(self,reduced_embeddings, incoming_csv_length):
        # Determine optimal number of clusters using silhouette score
        silhouette_scores = []
        range_n_clusters = range(2, incoming_csv_length // 10)

        for n_clusters in range_n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(reduced_embeddings)
            silhouette_avg = silhouette_score(reduced_embeddings, cluster_labels)
            silhouette_scores.append((silhouette_avg, n_clusters))

        # Choose the best number of clusters based on silhouette score
        optimal_silhouette_score, optimal_n_clusters = max(silhouette_scores, key=lambda x: x[0])  
        logging.info(f"Cluster number finding completed!!!!!!!!")
        logging.info(f"Optimal number of clusters based on silhouette score: {optimal_n_clusters} with a silhouette score of: {optimal_silhouette_score:.4f}")
        return optimal_n_clusters

    def train(self, file_path):
        df = pd.read_csv(file_path, encoding='latin1')
        incoming_csv_length = len(df["Short Description"])
        df = df.dropna(subset=["Short Description"])
        df.reset_index(drop=True, inplace=True)
        short_description_list = df["Short Description"].tolist()
        df["Cleaned_Description"] = preProcessingInstence.preprocess_data(short_description_list)
        self.df = df.copy() 
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
        if incoming_csv_length != self.current_csv_length:
            n_clusters = self.cluster_number(reduced_embeddings, incoming_csv_length)
            update_data('store/store.json','current_length', incoming_csv_length)
            update_data('store/store.json','n_clusters', n_clusters)
        else:
            n_clusters = self.n_cluster
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=46)
        self.cluster_assignments = self.kmeans_model.fit_predict(reduced_embeddings)
    
        # Save cluster assignments to a CSV file
        self.df['Cluster'] = self.cluster_assignments
        logging.info(f"Training completed!!!!!!!!")

    def save(self, filename):
        joblib.dump({
            'kmeans_model': self.kmeans_model,
            'scaler': self.scaler,
            'umap_reducer': self.umap_reducer,
            'cluster_assignments': self.cluster_assignments,
            'sentence_model': self.sentence_model,
            'df': self.df,
        }, filename)
