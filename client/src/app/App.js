import React from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { Home } from "../domain";
import Header from "./Header";
import { Stack } from "@mui/material";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  }
])

function App() {
  return (
    <div>
      <Header />
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
