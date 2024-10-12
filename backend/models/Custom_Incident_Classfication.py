import spacy
from nltk.corpus import stopwords
from nltk import download
import re
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data
download('stopwords')

class ClusteringModel:
    def __init__(self):
        self.kmeans_model = None
        self.scaler = None
        self.umap_reducer = None
        self.sentence_model = None
        self.cluster_assignments = None
        self.df = None

    def remove_before_colon(self, sentence):
        # Remove content before the first colon or "DVT:"
        sentence = sentence.split("DVT:", 1)[-1] if "DVT:" in sentence else sentence.split(":", 1)[-1]
        
        patterns = [
            r'\balizon(?:_?[a-zA-Z]?\d+)?\b',
            r'\bv\d{5}\b',
            r'\bv\d+\.\d+\.\d+(?:\.\d+)?\b'
        ]
        
        for pattern in patterns:
            sentence = re.sub(pattern, '', sentence)

        return sentence.strip()

    def predict(self, new_incident):
        # Preprocess the incoming incident
        preprocessed_incident = self.remove_before_colon(new_incident)
        nlp = spacy.load("en_core_web_sm")
        cleaned_incident_text = (preprocessed_incident.lower().strip())
        cleaned_incident_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_incident_text)
        tokenized_incident = [token.text for token in nlp(cleaned_incident_text)]
        stop_words = set(stopwords.words('english'))
        additional_stopwords = {'issue', 'poco', 'corvette14', 'corvette', 'pocowestern', 'error', 'problem', 
                                'zbook', 'western', 'probook', 'notebook', 'elitebook', 'elitedesk', 'dragonfly',
                                'pavilion', 'zbookfury'}
        stop_words.update(additional_stopwords)
        # Removing stopwords
        filtered_incident = [word for word in tokenized_incident if word not in stop_words]
        # Lemmatize
        lemmatized_incident = [token.lemma_ for token in nlp(' '.join(filtered_incident))]
        final_cleaned_incident = ' '.join(lemmatized_incident)

        # Encode the cleaned incident
        cleaned_incident_embedding = self.sentence_model.encode([final_cleaned_incident], convert_to_tensor=True)

        # Scale and reduce the incident embedding
        scaled_incident = self.scaler.transform(cleaned_incident_embedding.cpu().numpy())
        reduced_incident = self.umap_reducer.transform(scaled_incident)

        cluster = self.kmeans_model.predict(reduced_incident)
        return cluster[0]
    
    def get_predicted_cluster_items(self, new_incident):
        predicted_cluster= self.predict(new_incident)
        items_in_cluster = self.df[self.cluster_assignments == predicted_cluster][['Observation ID', 'Short Description']].values.tolist()
        return items_in_cluster
    
    def get_all_clusters(self):
        clusters= self.cluster_assignments
        df_incident = self.df["Short Description"].tolist()
        return clusters, df_incident

    def get_sorted_cluster_items_by_similarity(self, new_incident):
        cluster_items = self.get_predicted_cluster_items(new_incident)

        # Extract short descriptions for similarity calculation
        cluster_descriptions = [item[1] for item in cluster_items]  # Only take the 'Short Description'

        # Compute similarity between incoming incident and each item in the cluster
        incoming_embedding = self.sentence_model.encode([new_incident], convert_to_tensor=True)
        cluster_embeddings = self.sentence_model.encode(cluster_descriptions, convert_to_tensor=True)
        similarities = cosine_similarity(incoming_embedding.cpu().numpy(), cluster_embeddings.cpu().numpy()).flatten()

        # Combine items with their similarity scores
        items_with_scores = list(zip(cluster_items, similarities))  # Include Observation ID, Description, and similarity

        # Filter items with similarity score >= 0.6
        filtered_items_with_scores = [(item, score) for item, score in items_with_scores if round(score,2) >= 0.60]

        # Sort the filtered items by similarity score in descending order
        sorted_filtered_items_with_scores = sorted(filtered_items_with_scores, key=lambda x: x[1], reverse=True)

        return sorted_filtered_items_with_scores


    @classmethod
    def load(cls, filename):
       loaded_components = joblib.load(filename)
       model_instance = cls()
       model_instance.kmeans_model = loaded_components['kmeans_model']
       model_instance.scaler = loaded_components['scaler']
       model_instance.umap_reducer = loaded_components['umap_reducer']
       model_instance.sentence_model = loaded_components['sentence_model']
       model_instance.cluster_assignments = loaded_components['cluster_assignments']
       model_instance.df = loaded_components['df']
       return model_instance