import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";


function App() {

  // --------------------------------------------------
  // BASIC APPLICATION STATE
  // --------------------------------------------------

  // Store the current research question
  const [query, setQuery] = useState("");

  // Store the current AI answer
  const [answer, setAnswer] = useState("");

  // Store the current research sources
  const [sources, setSources] = useState([]);
  
  const [activity, setActivity] = useState([]);

  const [report, setReport] = useState("");

  // Store loading state
  const [loading, setLoading] = useState(false);
  
  // Store error message
  const [error, setError] = useState("");


  // --------------------------------------------------
  // RESEARCH HISTORY
  // --------------------------------------------------

  // Store previous research sessions
  const [history, setHistory] = useState(() => {

    // Try to read saved history from browser storage
    const savedHistory =
      localStorage.getItem("researchHistory");

    // If history exists, convert it from JSON to JavaScript
    if (savedHistory) {

      try {

        return JSON.parse(savedHistory);

      } catch {

        // Return empty history if saved data is invalid
        return [];
      }
    }

    // Start with an empty history
    return [];
  });


  // --------------------------------------------------
  // SAVE HISTORY TO LOCAL STORAGE
  // --------------------------------------------------

  useEffect(() => {

    // Convert history into JSON and save it
    localStorage.setItem(
      "researchHistory",
      JSON.stringify(history)
    );

  }, [history]);


  // --------------------------------------------------
  // EXTRACT WEBSITE DOMAIN
  // --------------------------------------------------

  const getDomain = (url) => {

    try {

      // Convert URL into URL object
      const website = new URL(url);

      // Return clean domain
      return website.hostname.replace("www.", "");

    } catch {

      // Fallback for invalid URLs
      return "Web Source";
    }
  };


  // --------------------------------------------------
  // START RESEARCH
  // --------------------------------------------------

  const handleResearch = async () => {

    // Clear previous error
    setError("");


    // Check for empty question
    if (!query.trim()) {

      setError("Please enter a research question.");

      return;
    }


    // Start loading
    setLoading(true);


    // Clear previous answer
    setAnswer("");

    // Clear previous sources
    setSources([]);


    
try {
  // Read the backend URL from the frontend environment file.
  // Use the local backend URL if the environment variable is unavailable.
  const API_URL =
    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  // Send the research request to the FastAPI backend.
  const response = await fetch(
    `${API_URL.replace(/\/+$/, "")}/research`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query: query
      })
    }
  );

  // Convert the backend response to JSON.
  const data = await response.json();

  // Check whether the backend returned an error.
  if (!response.ok) {
    throw new Error(
      data.detail || "Research request failed."
    );
  }

  // Save the research answer.
  setAnswer(data.answer);

  // Save the research sources.
  setSources(data.sources || []);

  // Save agent activity information.
  setActivity(data.activity || []);

  // Save the downloadable report content.
  setReport(data.report || "");

  // Create a new research history item.
  const historyItem = {
    id: Date.now(),
    query: query,
    answer: data.answer,
    sources: data.sources || [],
    date: new Date().toLocaleString()
  };

  // Add the new research item to the beginning of history.
  setHistory((previousHistory) => [
    historyItem,
    ...previousHistory
  ]);
}



    catch (error) {

      // Display error
      setError(
        error.message ||
        "Something went wrong while performing research."
      );

    }


    finally {

      // Stop loading
      setLoading(false);
    }
  };


  // --------------------------------------------------
  // LOAD PREVIOUS RESEARCH
  // --------------------------------------------------

  const loadHistory = (item) => {

    // Restore the previous question
    setQuery(item.query);

    // Restore the previous answer
    setAnswer(item.answer);

    // Restore previous sources
    setSources(item.sources || []);

    // Clear errors
    setError("");
  };


  // --------------------------------------------------
  // CLEAR HISTORY
  // --------------------------------------------------

  const clearHistory = () => {

    // Remove all history items
    setHistory([]);

  };


  // --------------------------------------------------
  // FRONTEND
  // --------------------------------------------------

  return (

    <div className="app">


      {/* ============================================
          HEADER
      ============================================ */}

      <header className="header">

        <div className="brand">

          <div className="logo">
            🔎
          </div>

          <div>

            <h1>
              AI Research Assistant
            </h1>

            <p>
              Search the web. Analyze sources. Get AI-powered research.
            </p>

          </div>

        </div>

      </header>



      {/* ============================================
          MAIN LAYOUT
      ============================================ */}

      <main className="main-layout">


        {/* ==========================================
            HISTORY SIDEBAR
        ========================================== */}

        <aside className="history-sidebar">

          <div className="history-header">

            <div>

              <h2>
                🕘 Research History
              </h2>

              <p>
                {history.length} saved research
                {history.length === 1 ? "" : "es"}
              </p>

            </div>


            {history.length > 0 && (

              <button
                className="clear-history"
                onClick={clearHistory}
              >
                Clear
              </button>

            )}

          </div>


          {/* History list */}

          {history.length === 0 ? (

            <div className="empty-history">

              <div className="empty-icon">
                📚
              </div>

              <p>
                Your previous research questions
                will appear here.
              </p>

            </div>

          ) : (

            <div className="history-list">

              {history.map((item) => (

                <button
                  className="history-item"
                  key={item.id}
                  onClick={() => loadHistory(item)}
                >

                  <span className="history-question">

                    {item.query}

                  </span>

                  <span className="history-date">

                    {item.date}

                  </span>

                </button>

              ))}

            </div>

          )}

        </aside>



        {/* ==========================================
            MAIN RESEARCH AREA
        ========================================== */}

        <section className="research-area">


          {/* ========================================
              SEARCH CARD
          ======================================== */}

          <section className="search-card">

            <div className="search-header">

              <span className="search-icon">
                🔬
              </span>

              <div>

                <h2>
                  Research a Topic
                </h2>

                <p className="description">

                  Ask a question and the AI assistant
                  will search the web, analyze multiple
                  sources, and generate a research-based
                  answer.

                </p>

              </div>

            </div>


            <textarea

              value={query}

              onChange={(event) =>
                setQuery(event.target.value)
              }

              placeholder="Example: What are the latest developments in AI agents?"

              rows="5"

            />


            <button

              className="research-button"

              onClick={handleResearch}

              disabled={loading}

            >

              {loading ? (

                <>
                  <span className="button-spinner"></span>
                  Researching...
                </>

              ) : (

                <>
                  🔎 Start Research
                </>

              )}

            </button>


            {/* Error */}

            {error && (

              <div className="error">

                ⚠️ {error}

              </div>

            )}

          </section>



          {/* ========================================
              LOADING
          ======================================== */}

          {loading && (

            <section className="loading-card">

              <div className="spinner"></div>

              <h3>
                Researching the web...
              </h3>

              <p>
                Searching multiple sources and
                generating your AI research answer.
              </p>

            </section>

          )}
          
          {activity.length > 0 && (
  <div className="activity-section">

    <h3>🤖 Agent Activity</h3>

    <div className="activity-list">

      {activity.map((item) => (

        <div
          key={item.step}
          className="activity-item"
        >

          <div className="activity-icon">

            {item.type === "planning" && "🧠"}

            {item.type === "search" && "🔎"}

            {item.type === "sources" && "📚"}

            {item.type === "synthesis" && "🤖"}

          </div>

          <div className="activity-content">

            <div className="activity-title">
              {item.title}
            </div>

            <div className="activity-description">
              {item.description}
            </div>

          </div>

          <div className="activity-status">
            ✓
          </div>

        </div>

      ))}

    </div>

  </div>
)}

{/* ========================================
    DOWNLOAD REPORT
======================================== */}

{report && !loading && (

  <div className="report-section">

    <button
      className="download-report-button"
      onClick={() => {

        const blob = new Blob(
          [report],
          {
            type: "text/markdown"
          }
        );

        const url = URL.createObjectURL(
          blob
        );

        const link =
          document.createElement("a");

        link.href = url;

        link.download =
          "AI_Research_Report.md";

        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);

        URL.revokeObjectURL(url);

      }}
    >

      📄 Download Research Report

    </button>

  </div>

)}


          {/* ========================================
              AI ANSWER
          ======================================== */}

          {answer && !loading && (

            <section className="answer-card">

              <div className="section-heading">

                <span className="section-icon">
                  🤖
                </span>

                <div>

                  <h2>
                    AI Research Answer
                  </h2>

                  <p className="section-subtitle">
                    Generated from web research
                  </p>

                </div>

              </div>


              <div className="answer-content">

                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                >

                  {answer}

                </ReactMarkdown>

              </div>

            </section>

          )}



          {/* ========================================
              SOURCES
          ======================================== */}

          {sources.length > 0 && !loading && (

            <section className="sources-card">

              <div className="section-heading">

                <span className="section-icon">
                  📚
                </span>

                <div>

                  <h2>
                    Research Sources
                  </h2>

                  <p className="section-subtitle">
                    Web sources used to generate the answer
                  </p>

                </div>

              </div>


              <div className="source-summary">

                <span className="source-count-badge">
                  {sources.length}
                </span>

                <span>
                  Sources analyzed
                </span>

              </div>


              <div className="sources-list">

                {sources.map((source, index) => (

                  <article
                    className="source"
                    key={index}
                  >

                    <div className="source-number">

                      {index + 1}

                    </div>


                    <div className="source-content">

                      <div className="source-top">

                        <h3>
                          {source.title || "Untitled Source"}
                        </h3>

                        <span className="source-domain">

                          🌐 {getDomain(source.url)}

                        </span>

                      </div>


                      <p className="source-description">

                        {source.content ||
                          "No description available."
                        }

                      </p>


                      <a

                        className="source-button"

                        href={source.url}

                        target="_blank"

                        rel="noopener noreferrer"

                      >

                        Open Source
                        <span>↗</span>

                      </a>

                    </div>

                  </article>

                ))}

              </div>

            </section>

          )}

        </section>

      </main>



      {/* ============================================
          FOOTER
      ============================================ */}

      <footer className="footer">

        <p>
          AI Research Assistant
        </p>

        <span>
          React • FastAPI • Tavily • Ollama
        </span>

      </footer>

    </div>
  );
}


export default App;