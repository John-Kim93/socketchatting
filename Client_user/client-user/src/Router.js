import React from "react";
import {
  QueryClient,
  QueryClientProvider,
} from 'react-query'
import { BrowserRouter, Route, Routes } from "react-router-dom";
import './global.css';
import { ColorModeProvider } from "@chakra-ui/react"
import NotFound from "./NotFound"
import Home from "./pages/Home"
import Talk from "./pages/Talk"
import Lobby from "./pages/Lobby";

export default function Router() {
  const [queryClient] = React.useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        // staleTime: 30 * 60 * 1000,
        cacheTime: 2 * 60 * 60 * 1000,
      },
    }
  }))

  return (
    <ColorModeProvider>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/lobby" element={<Lobby />} />
            <Route path="/talk/:roomID" element={<Talk />} />
            <Route path="/*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ColorModeProvider>
  )
}