import React, { createContext, useContext, useEffect, useState } from "react";
import IncidentForm from "./pages/IncidentForm";
import { createTheme, ThemeProvider } from "@mui/material";
import Tabs from "./components/tab/Tabs";
import IncidentClusters from "./pages/IncidentClusters";
import "./App.css";

export const MyContext = createContext();

const theme = createTheme({
  palette: {
    mode: "dark",
    background: {
      default: "#121212",
      paper: "#1e1e1e",
    },
    text: {
      primary: "#ffffff",
      secondary: "#b0bec5",
    },
  },
});

const tabData = [{ label: "Search" }, { label: "Clusters" }];

const App = () => {
  const [activeTab, setActiveTab] = useState("Search"); // State to track the active tab

  const handleTabChange = (tab) => {
    console.log(tab);
    setActiveTab(tab);
  };

  const renderComponent = () => {
    switch (activeTab) {
      case "Search":
        return <IncidentForm />;
      case "Clusters":
        return <IncidentClusters />;
      default:
        return null;
    }
  };

  return (
    <>
      <MyContext.Provider
        value={{ activeTab, setActiveTab, message: renderComponent() }}
      >
        <ThemeProvider theme={theme}>
          <Tabs tabs={tabData} onChange={handleTabChange} />
          <MyComponent />
        </ThemeProvider>
      </MyContext.Provider>
    </>
  );
};

const MyComponent = () => {
  const { message } = useContext(MyContext);
  return <div>{message}</div>;
};

export default App;
