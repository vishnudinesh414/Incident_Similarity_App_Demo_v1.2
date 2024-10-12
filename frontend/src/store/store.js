import { makeAutoObservable } from "mobx";

class IncidentStore {
  clusters = [];
  incidents = [];
  similarIncidents = [];
  currentIncident = "";
  CLUSTERS = "Cluster : ";
  SIMILIAR_INCIDENTS = "Similar Incidents : ";
  PAGE_TYPE = {
    CLUSTERS: "cluster_list",
    INCIDENTS: "incident_list",
  };

  constructor() {
    makeAutoObservable(this);
  }

  setClusters = (clusters) => {
    this.clusters = clusters;
  };

  setIncidents = (incidents) => {
    this.incidents = incidents;
  };
  setSimilarIncidents = (similarIncidents) => {
    this.similarIncidents = similarIncidents;
  };
  setCurrentIncident = (currentIncident) => {
    this.currentIncident = currentIncident;
  };
}

const incidentStore = new IncidentStore();
export default incidentStore;
