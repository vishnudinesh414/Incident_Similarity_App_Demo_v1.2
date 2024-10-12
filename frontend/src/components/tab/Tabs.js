import React, { useState } from "react";
import Tab from "./Tab";
import "./Tabs.css";

const Tabs = ({ tabs, onChange }) => {
  const [activeTab, setActiveTab] = useState(tabs[0].label);

  const handleTabClick = (event, label) => {
    event.preventDefault();
    setActiveTab(label);
    onChange(label);
  };

  return (
    <div className="tabs-container">
      <div className="tabs">
        {tabs.map((tab) => (
          <Tab
            key={tab.label}
            label={tab.label}
            isActive={activeTab === tab.label}
            onClick={(event) => handleTabClick(event, tab.label)}
          />
        ))}
      </div>
    </div>
  );
};

export default Tabs;
