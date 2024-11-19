import type { MetaFunction } from "@remix-run/node";

import React, { createContext, useContext, useState } from 'react';
import { SidebarProvider } from '~/components/SidebarContext';



export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};



import Sidebar from '~/components/sidebar'
import Topic from '~/routes/$topic'
import 'app/css/global-styles.css'







/* ----------------------------------------------------------------- */


export default function Index() {
  
  const [activeTopic, setActiveTopic] = useState<string>('science');

  return (
    <div className="app-container">
      <SidebarProvider>
        <div className="main-page">
          <div>
            header
          </div>
          <div className="bottom">
            <Sidebar setActiveTopic={ setActiveTopic } />
            <Topic setActiveTopic={ setActiveTopic }/>
          </div>
        </div>
      </SidebarProvider>
      
    </div>
  );
}
