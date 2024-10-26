from training.training_model import ClusterTrainingingModel

if __name__ == "__main__":
    model = ClusterTrainingingModel()
    model.train('data/new_pseudonymized_in.csv')
    model.save('models/K-Mean_MiniLM-Custom_Incident_Classification_Model.pkl')