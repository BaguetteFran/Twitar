import { ActionFunction, json, redirect } from "@remix-run/node";
import { PrismaClient } from "@prisma/client";
import { composeEventHandlers } from "@remix-run/react/dist/components";

const prisma = new PrismaClient();


export const action: ActionFunction = async ({request}) => { 
    console.log("In action starting");
    const formData = await request.formData();
    const post_id = formData.get("post_id");
    const post_score = Number(formData.get("score"));

    console.log(post_score);

    if (!post_id || typeof post_id !== "string") {
        return new Response("Error: Invalid or missing post_id", { status: 400 });
    }
    if (!post_score) { 
        return new Response("Error: Invalid or missing post_id", { status: 400 });
    }
    const score = Number(post_score);

    try { 
        await prisma.tweets.update({
            where: {id: post_id}, // it is a string rn keep it that way change the db
            data: {score: Number(score)}, 
        });


        return new Response("Score updated succefully", {status : 200});

    } catch(error) { 
        console.error("error updating score in action function", error);
        return new Response("Error updating score in action functon", {status : 500});
    }

}