import React, { useState } from "react";
import axios from "axios";
import "./IncidentForm.css";
import incidentStore from "../store/store";
import IncidentTable from "../components/table/IncidentTable";

const Incidentsimilarity = () => {
  const [incident, setIncident] = useState(incidentStore.currentIncident);
  const [similarIncidents, setSimilarIncidents] = useState(
    incidentStore.similarIncidents
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await axios.post("http://localhost:5000/api/predict", {
        incident,
      });
      setSimilarIncidents(data.similar_incidents);
      incidentStore.setSimilarIncidents(data.similar_incidents);
      incidentStore.setCurrentIncident(incident);
    } catch (error) {
      console.error("Error submitting incident:", error);
    }
  };

  const similar_incident_payload = {
    type: incidentStore.PAGE_TYPE.INCIDENTS,
    data: { incidents: similarIncidents },
    heading: incidentStore.SIMILIAR_INCIDENTS,
  };

  return (
    <div className="outer_page">
      <h1 className="heading">Incident Similarity App</h1>
      <form className="form-container" onSubmit={handleSubmit}>
        <label htmlFor="incident" className="label">
          Enter the Incident
        </label>
        <textarea
          id="incident"
          className="textarea"
          value={incident}
          onChange={(e) => setIncident(e.target.value)}
          placeholder="Enter the incident..."
          rows="6"
          cols="80"
          required
        />
        <div className="button-container">
          <button type="submit" className="submit-button">
            Submit
          </button>
        </div>
      </form>

      {similarIncidents.length > 0 && (
        <IncidentTable
          payload={similar_incident_payload}
        />
      )}
    </div>
  );
};

export default Incidentsimilarity;
