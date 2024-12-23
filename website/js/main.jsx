import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Gallery from "./gallery";

// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the gallery component into the DOM
root.render(
  <StrictMode>
    <Gallery />
  </StrictMode>,
);
