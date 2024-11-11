
import { Tweet } from "app/interfaces/tweet_inter"
import { Fragment } from "react/jsx-runtime"
import "app/css/tweet_stream_css.css"
import { useFetcher } from "@remix-run/react";
import { UploadHandler } from "@remix-run/node";
import React, { RefObject, useEffect, useRef, useState } from "react";
import { faSortNumericAsc } from "@fortawesome/free-solid-svg-icons";


interface TweetDataProps { 
    tweet_data: Tweet[]
}

interface ScoreHandle { 
    score: string;
    post_id: string;
}





export default function TweetStrem({tweet_data} : TweetDataProps ) { 

    const fetcher = useFetcher();
    const tweetRefs = useRef<RefObject<HTMLLIElement>[]>([]); //assigns an empty ref array and it has the property .current to it 
    const inputRefs = useRef<RefObject<HTMLInputElement>[]>([]);
    const [currentTweetIndex, setCurrentTweetIndex] = useState(0);




    tweetRefs.current = tweet_data.map((_,i) => tweetRefs.current[i] ?? React.createRef<HTMLDivElement>() ); //creating a ref for each tweet 
    inputRefs.current = tweet_data.map((_,i) => inputRefs.current[i] ?? React.createRef<HTMLInputElement>());

    console.log(tweetRefs.current.length);
    console.log("Current tweet index : ", currentTweetIndex);
    



    const handleSubmitScore = ({ score, post_id }: ScoreHandle) => {

        const numericScore = Number(score);

        
        
        const formData = new FormData();
        formData.append("score", String(score));
        formData.append("post_id", post_id);
        
        console.log("Submitting fetcher....");

        fetcher.submit(
            formData, 
            {method:"post", 
            action:"/submit_score"
        },
        );
    }




    useEffect(()=> { 


        if (fetcher.state === 'idle') { 
            console.log("we are ok in teh index changer..... it is about to go. did it ");
            setCurrentTweetIndex(currentTweetIndex => Math.min(currentTweetIndex + 1, tweet_data.length - 1));   
            console.log("YES");
        }
    }, [fetcher.state]);




    useEffect(() => { 

        const currentRef = tweetRefs.current[currentTweetIndex]?.current;
        const currentInputRef = inputRefs.current[currentTweetIndex]?.current;


        if (currentRef) {
            currentRef.scrollIntoView({
                behavior: "smooth",
                block: "start",
            });
        }

        if (currentInputRef) { 
            currentInputRef.focus();
        }

    }, [currentTweetIndex]);
    



    return ( 

        <div className="post_stream">
            <p>hello</p>
                <ul>
                    {tweet_data.map((post:Tweet, index) => (
                        <li key={post.id} ref={tweetRefs.current[index]} >

                                <div className="post">
                                    <div className="head">
                                        <div className="profile_img_div">
                                            {post.profile_img && 
                                                <img className="profile_img" src={post.profile_img} alt='profile_img'></img>
                                            }
                                        </div>
                                        <div className="user_name">
                                            {post.screen_name && 
                                                <h1>{post.screen_name}</h1>
                                            }
                                        </div>
                                        <div className="number">
                                            {post.score && 
                                                <p><b>{post.score}</b></p>
                                            }
                                        </div>
                                        <div className="grader">
                        
                                            <input type='hidden' name="post_id"  value={post.id}></input>
                                            <label>
                                                Score:
                                                <input ref={inputRefs.current[index]} className="input-class" type="number" name="score" required 
                                                onKeyDown={(e) => {
                                                    if (e.key === "Enter") {
                                                        const target = e.target as HTMLInputElement; //neeed as HTML input element beacuse e can be anything and typse need toknow it is input iwth value 
                                                        handleSubmitScore({score: target.value, post_id: post.id});
                                                    }
                                                }}
                                                />
                                                
                                            </label>
                                            
                                        </div>
                                        
                                    </div>
                                    <div className="text">
                                        {post.text && 
                                            <p> {post.text} </p>
                                        }

                                    </div>
                                    <div className="media">
                                        {post.img_url &&
                                        <img src={post.img_url} alt="post-img"></img>
                                        }
                                    </div>

                                </div>


                        </li>
                    )
                    

                    )}

                </ul>
        </div>
    );
}

function setErrorMessage(arg0: string) {
    throw new Error("Function not implemented.");
}
