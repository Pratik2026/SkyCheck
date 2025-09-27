import React, { useState } from "react";
import ChatInterface from "./components/chat/chatInterface";
import "./App.css";
import Header from "./components/Header";
import DoodleBackground from "./components/chat/doodleBackground";
import { ToastContainer } from "react-toastify";

function App() {
  const [language, setLanguage] = useState("english");

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
  };

  return (
    <div className="min-h-screen flex flex-col text-foreground transition-colors ">
      {/* Header */}
      <Header language={language} onLanguageChange={handleLanguageChange} />
      <DoodleBackground opacity={0.035}>
        <ChatInterface
          className="flex-1 flex flex-col min-h-full"
          language={language}
          onLanguageChange={handleLanguageChange}
        />
      </DoodleBackground>
      <ToastContainer position="top-center" autoClose={3000}/>
    </div>
  );
}

export default App;