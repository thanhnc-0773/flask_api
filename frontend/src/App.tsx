import React from "react";
import "./App.css";
import RoutesApp from "./routes/index.routes";
import ResetScroll from "./components/atoms/ResetScroll";

function App() {
  return (
    <>
      <ResetScroll />
      <RoutesApp />
    </>
  );
}

export default App;
