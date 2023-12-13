import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [htmlContent, setHtmlContent] = useState({ __html: "Loading..." });

  useEffect(() => {
    // Fetch the HTML content when the component mounts
    fetch('/webber') // Adjust the endpoint if necessary
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then((html) => {
        setHtmlContent({ __html: html });
      })
      .catch((error) => {
        console.error('Error fetching the HTML:', error);
        setHtmlContent({ __html: "Failed to load content." });
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {/* This will render the fetched HTML content */}
        <div dangerouslySetInnerHTML={htmlContent} />
      </header>
    </div>
  );
}

export default App;
