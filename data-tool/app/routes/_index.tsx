import type { MetaFunction } from "@remix-run/node";
import { PrismaClient } from "@prisma/client";
import { json } from "@remix-run/node";

import TweetStream from "~/components/tweet_stream";
import { Tweet } from "app/interfaces/tweet_inter.js";
import { useLoaderData } from "@remix-run/react";

export const meta: MetaFunction = () => {
  return [{ title: "Get Workin" }, { name: "work", content: "Welcome Home" }];
};

const prisma = new PrismaClient();

export async function loader() {
  const tweet_data: Tweet[] = await prisma.posts.findMany();
  return new Response(JSON.stringify(tweet_data), {
    headers: {
      "Content-Type": "application/json", // Set the content type to JSON
    },
  });
}

export default function Index() {
  const tweet_data = useLoaderData<Tweet[]>();

  return <TweetStream tweet_data={tweet_data}></TweetStream>;
}
