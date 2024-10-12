// IncidentTable.js
import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
} from "@mui/material";

const IncidentTable = ({ payload }) => {
  const uniqueClusters = [...new Set(payload.data.clusters)].sort(
    (a, b) => a - b
  );
  return (
    <div className="similar-incidents-container">
      <h3 className="similar-incidents-heading">{payload.heading}</h3>
      <TableContainer component={Paper} style={{ marginTop: "20px" }}>
        <Table sx={{ minWidth: 650 }} aria-label="similar incidents table">
          <TableHead>
            <TableRow>
              {payload.type === "incident_list" ? (
                <>
                  <TableCell>
                    <Typography variant="h6">ID</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="h6">Description</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="h6">Similarity Score</Typography>
                  </TableCell>
                </>
              ) : (
                <>
                  <TableCell>
                    <Typography variant="h6">Cluster ID</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="h6">Incidents</Typography>
                  </TableCell>
                </>
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {payload.type === "incident_list"
              ? payload.data.incidents.map(
                  ([observationId, description, score], index) => (
                    <TableRow key={observationId} hover>
                      <TableCell>{observationId}</TableCell>
                      <TableCell>{description}</TableCell>
                      <TableCell>{score.toFixed(2)}</TableCell>
                    </TableRow>
                  )
                )
              : uniqueClusters.map((clusterId) => (
                  <TableRow key={clusterId}>
                    <TableCell component="th" scope="row">
                      Cluster {clusterId}
                    </TableCell>
                    <TableCell>
                      <ul className="incident-list">
                        {payload.data.incidents.map((incident, index) =>
                          payload.data.clusters[index] === clusterId ? (
                            <li key={index} className="incident-item">
                              {" "}
                              {incident}
                            </li>
                          ) : null
                        )}
                      </ul>
                    </TableCell>
                  </TableRow>
                ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default IncidentTable;
