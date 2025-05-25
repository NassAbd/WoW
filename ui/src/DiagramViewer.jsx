import { useState, useRef, useEffect } from "react";
import axios from "axios";
import mermaid from "mermaid";

mermaid.initialize({ startOnLoad: false });

function DiagramViewer() {
  const [module, setModule] = useState(() => localStorage.getItem("module") || "");
  const [diagrams, setDiagrams] = useState(() => {
    const saved = localStorage.getItem("diagrams");
    return saved ? JSON.parse(saved) : [];
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const containerRefs = useRef([]);

  const fetchDiagram = async () => {
    setError("");
    setDiagrams([]);
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/api/diagram", { module });
      if (res.data.error) {
        setError(res.data.error);
      } else {
        setDiagrams(res.data);

        // Sauvegarde dans le localStorage
        localStorage.setItem("diagrams", JSON.stringify(res.data));
        localStorage.setItem("module", module);
      }
    } catch (e) {
      setError("Erreur réseau ou serveur : " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      fetchDiagram();
    }
  };

  useEffect(() => {
    diagrams.forEach((d, i) => {
      if (containerRefs.current[i]) {
        mermaid
          .render(`mermaid-${i}`, d.diagram)
          .then(({ svg }) => {
            containerRefs.current[i].innerHTML = svg;
          })
          .catch((err) => {
            containerRefs.current[i].innerHTML = `<pre style="color: red;">Erreur Mermaid: ${err}</pre>`;
          });
      }
    });
  }, [diagrams]);

  return (
    <div className="diagram-viewer">
      <div className="input-group">
        <input
          value={module}
          onChange={(e) => setModule(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Module name (allianz, bp, etc)"
          className="input"
          disabled={loading}
        />
        <button onClick={fetchDiagram} className="button" disabled={loading}>
          {loading ? "Loading..." : "Generate"}
        </button>
      </div>

      {loading && (
        <div className="loading-spinner">
          <div className="spinner" />
          <span>Generating diagram...</span>
        </div>
      )}

      {error && <div className="error-message">⚠️ {error}</div>}

      {diagrams.map((d, i) => (
        <div key={i} className="diagram-block">
          <h3 className="diagram-title">{d.root}</h3>
          <div
            className="diagram-container"
            ref={(el) => (containerRefs.current[i] = el)}
          />
        </div>
      ))}
    </div>
  );
}

export default DiagramViewer;
