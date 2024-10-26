import re
import spacy
from nltk.corpus import stopwords
import pandas as pd
from pathlib import Path

class IncidentPreProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.additional_stopword_path = "data/additional_stopwords.txt"

        self.stopwords = self.get_stopwords()

    def cleanup_data(self, sentence):
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

    def preprocess_data(self, incidentList):
        # Convert to Pandas Series if input is a list or string
        if isinstance(incidentList, list):
            incidentList = pd.Series(incidentList)
        elif isinstance(incidentList, str):
            incidentList = pd.Series([incidentList])

        # Clean and tokenize descriptions in one go using a single apply function
        cleanedIncidentList = (
            incidentList
            .apply(self.cleanup_data)
            .str.lower()
            .str.strip()
            .str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
            .apply(lambda x: [token.text for token in self.nlp(x)])
            .apply(lambda x: [word for word in x if word not in self.stopwords])
            .apply(lambda x: [token.lemma_ for token in self.nlp(' '.join(x))])
            .apply(lambda x: ' '.join(x))
        )
        
        return cleanedIncidentList.tolist() 

    def get_stopwords(self):
        stop_words = set(stopwords.words('english'))

        additional_stopwords = set()
        try:
            with open(self.additional_stopword_path, 'r') as file:
                for line in file:
                    additional_stopwords.add(line.strip())
        except FileNotFoundError:
            print("Warning: additional_stopwords.txt not found. Using default additional stopwords.")
        
        stop_words.update(additional_stopwords)
        return stop_words