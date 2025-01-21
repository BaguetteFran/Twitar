import type { MetaFunction } from "@remix-run/node";

import React, { createContext, useContext, useState } from 'react';
import { SidebarProvider } from '~/components/SidebarContext';

import Sidebar from '~/components/sidebar'
import Topic from '~/routes/$topic'
import 'app/css/global-styles.css'
import { PrismaClient } from "@prisma/client";
import { Tweet } from "~/interfaces/tweet_interface";
import  TweetStream  from '~/components/main_stream'
import { useLoaderData } from "@remix-run/react";

export const meta: MetaFunction = () => {
  return [
    { title: "Get Workin" },
    { name: "work", content: "Welcome Home" },
  ];
};



const prisma = new PrismaClient();

export async function loader() {
  const tweet_data: Tweet[] = await prisma.tweets.findMany();
  return tweet_data; // Remix will handle serialization automatically
}




/* ----------------------------------------------------------------- */


export default function Index() {
  
  const [activeTopic, setActiveTopic] = useState<string>('science');  
  const tweet_data = useLoaderData<Tweet[]>();

  return (
    <div className="app-container">
      <SidebarProvider>
        <div className="main-page">
          <div>
            header
          </div>
          <div className="bottom">
            <Sidebar setActiveTopic={ setActiveTopic } />
            <TweetStream data={tweet_data}></TweetStream>
          </div>
        </div>
      </SidebarProvider>
      
    </div>
  );
}
function useLoaderFunction<T>() {
  throw new Error("Function not implemented.");
}

