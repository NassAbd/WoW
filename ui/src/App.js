import DiagramViewer from "./DiagramViewer";
import "./App.css"; // fichier CSS associé

function App() {
  return (
    <div className="app-container">
      <div className="app-content">
        <h1 className="app-title">Woob Object Watcher</h1>
        <h3 className="app-subtitle">W.O.W</h3>
        <DiagramViewer />
      </div>
    </div>
  );
}

export default App;
