import React, { createContext, useContext, useState } from 'react';

// Create a Context for the sidebar state
const SidebarContext = createContext<any>(null);

// Custom hook to use the Sidebar context
export const useSidebar = () => useContext(SidebarContext);

export const SidebarProvider = ({ children }: { children: React.ReactNode }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <SidebarContext.Provider value={{ isSidebarOpen, setIsSidebarOpen }}>
      {children}
    </SidebarContext.Provider>
  );
};
