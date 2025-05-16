import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import { Agent } from "./Agent";
import { Banners } from "./Banners";

export function Router() {
  return (
    <BrowserRouter basename="index.html">
      <Routes>
        <Route index element={<Navigate to="banners" />} />
        <Route path="*" element={<Navigate to="banners" />} />
        <Route path="banners" element={<Banners />} />
        <Route path="agent" element={<Agent />} />
      </Routes>
    </BrowserRouter>
  );
}
