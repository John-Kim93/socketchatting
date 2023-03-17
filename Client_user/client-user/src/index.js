import React from 'react';
import ReactDOM from 'react-dom/client';
import Router from "./Router";

// ReactDOM.render(<Router />, document.getElementById("root"));

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <Router />
  </React.StrictMode>
);