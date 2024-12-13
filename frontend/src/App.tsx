import React from "react";
import "./App.css";
import RoutesApp from "./routes/index.routes";
import ResetScroll from "./components/atoms/ResetScroll";

function App() {
  console.log(process.env.NODE_ENV === "production");

  if (process.env.NODE_ENV === "production") {
    const originalConsoleWarn = console.warn;
    console.warn = (...args) => {
      console.log({ args });

      if (args[0] && args[0].includes("ResizeObserver loop completed with undelivered notifications")) {
        return;
      }
      originalConsoleWarn(...args);
    };
  }

  if (process.env.NODE_ENV === "production") {
    const originalResizeObserver = window.ResizeObserver;

    window.ResizeObserver = class ResizeObserverMock {
      observe() {}
      unobserve() {}
      disconnect() {}
    };
  }

  return (
    <>
      <ResetScroll />
      <RoutesApp />
    </>
  );
}

export default App;
