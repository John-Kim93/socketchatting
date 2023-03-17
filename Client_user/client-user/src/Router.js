import React from "react";
import {
  QueryClient,
  QueryClientProvider,
} from 'react-query'
import { BrowserRouter, Route, Routes } from "react-router-dom";
import './global.css';
import { ColorModeProvider } from "@chakra-ui/react"
import Home from "./pages/Home"
import NotFound from "./NotFound"

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
            <Route path="/*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ColorModeProvider>
  )
}