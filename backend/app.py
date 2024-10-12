# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from models.Custom_Incident_Classfication import ClusteringModel
import numpy as np

app = Flask(__name__)
CORS(app)

# Load your trained model
model = ClusteringModel.load('models/K-Mean_MiniLM-Custom_Incident_Classification_Model.pkl')  # Replace with your model filename

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    incident = data.get('incident')

    if not incident:
        return jsonify({'error': 'No incident provided'}), 400

    similar_incidents = model.get_sorted_cluster_items_by_similarity(incident)

    # Convert similar_incidents to a standard format including Observation ID, Short Description, and similarity score
    similar_incidents = [(item[0][0], item[0][1], float(item[1])) for item in similar_incidents]

    return jsonify({
        'similar_incidents': similar_incidents
    })

@app.route('/api/clusters', methods=['GET'])
def get_clusters():
    all_clusters,df_incident = model.get_all_clusters()
    
    # Convert all clusters to a list if they are numpy arrays
    if isinstance(all_clusters, np.ndarray):
        all_clusters = all_clusters.tolist()
    elif isinstance(all_clusters, (list, tuple)):
        all_clusters = [item.tolist() if isinstance(item, np.ndarray) else item for item in all_clusters]

    print(set(all_clusters))
    return jsonify({
        'clusters': all_clusters,
        'incidents': df_incident
    })

    
if __name__ == '__main__':
    app.run(debug=True)