import React, { useState } from "react";
import "./App.css";
import Header from "./components/Header";
function App() {
  const [language, setLanguage] = useState("english");

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
  };

  return (
    <div className="min-h-screen flex flex-col text-foreground transition-colors ">
      {/* Header */}
      <Header language={language} onLanguageChange={handleLanguageChange} />
  
    </div>
  );
}

export default App;
