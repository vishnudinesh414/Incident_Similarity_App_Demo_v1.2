import React, { useEffect, useState } from "react";
import { observer } from "mobx-react";
import axios from "axios";
import IncidentStore from "../store/store";
import IncidentTable from "../components/table/IncidentTable";
import incidentStore from "../store/store";

const IncidentClusters = observer(() => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [clusters, setClusters] = useState(IncidentStore.clusters);
  const [incidents, setIncidents] = useState(IncidentStore.incidents);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/clusters");
        setClusters(response.data.clusters);
        setIncidents(response.data.incidents);
        IncidentStore.setClusters(response.data.clusters);
        IncidentStore.setIncidents(response.data.incidents);
      } catch (error) {
        console.error("Error fetching incidents:", error);
        setError("Failed to load incident clusters.");
      } finally {
        setLoading(false);
      }
    };
    if (clusters.length === 0 && incidents.length === 0) {
      setLoading(true);
      fetchData();
    } else {
      setLoading(false);
    }
  }, []);

  const cluster_payload = {
    type: incidentStore.PAGE_TYPE.CLUSTERS,
    data: { clusters: clusters, incidents: incidents },
    heading: incidentStore.CLUSTERS,
  };

  return (
    <div className="outer_page">
      <div></div>
      {loading ? (
        <div>Loading...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : (
        incidents.length != 0 && <IncidentTable payload={cluster_payload} />
      )}
    </div>
  );
});

export default IncidentClusters;
