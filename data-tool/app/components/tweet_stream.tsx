import { Tweet } from "app/interfaces/tweet_inter";
import { Fragment } from "react/jsx-runtime";
import "app/css/tweet_stream_css.css";
import { useFetcher } from "@remix-run/react";
import { UploadHandler } from "@remix-run/node";
import React, { RefObject, useEffect, useRef, useState } from "react";
import { faSortNumericAsc } from "@fortawesome/free-solid-svg-icons";

interface TweetDataProps {
  tweet_data: Tweet[];
}

interface ScoreHandle {
  score: string;
  post_id: Number;
}

export default function TweetStrem({ tweet_data }: TweetDataProps) {
  const fetcher = useFetcher();
  const tweetRefs = useRef<RefObject<HTMLLIElement>[]>([]); //assigns an empty ref array and it has the property .current to it
  const inputRefs = useRef<RefObject<HTMLInputElement>[]>([]);
  const [currentTweetIndex, setCurrentTweetIndex] = useState(0);

  tweetRefs.current = tweet_data.map(
    (_, i) => tweetRefs.current[i] ?? React.createRef<HTMLDivElement>()
  ); //creating a ref for each tweet
  inputRefs.current = tweet_data.map(
    (_, i) => inputRefs.current[i] ?? React.createRef<HTMLInputElement>()
  );

  const handleSubmitScore = ({ score, post_id }: ScoreHandle) => {
    const formData = new FormData();
    formData.append("score", score);
    formData.append("post_id", String(post_id));

    fetcher.submit(formData, { method: "post", action: "/submit_score" });
  };

  useEffect(() => {
    if (fetcher.state === "idle") {
      setCurrentTweetIndex((currentTweetIndex) =>
        Math.min(currentTweetIndex + 1, tweet_data.length - 1)
      );
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
        {tweet_data.map((post: Tweet, index) => {
          let json_data = [];
          let media_data = [];

          try {
            json_data = post.media ? JSON.parse(post.media) : [];

            if (json_data.length > 0) {
              media_data = json_data[0]; // Assign the first object
            } else {
              media_data = []; // Assign an empty array if no media data
            }
          } catch (error) {
            console.error("Error parsing media JSON:", error);
          }

          return (
            <li key={post.id} ref={tweetRefs.current[index]}>
              <div className="post">
                <div className="head">
                  <div className="profile_img_div">
                    {post.avatar && (
                      <img
                        className="profile_img"
                        src={post.avatar}
                        alt="profile_img"
                      ></img>
                    )}
                  </div>
                  <div className="user_name">
                    {post.handle && <h1>{post.handle}</h1>}
                  </div>
                  <div className="number">
                    {post.score && (
                      <p>
                        <b>{post.score}</b>
                      </p>
                    )}
                  </div>
                  <div className="grader">
                    <input type="hidden" name="post_id" value={post.id}></input>
                    <label>
                      Score:
                      <input
                        ref={inputRefs.current[index]}
                        className="input-class"
                        type="number"
                        name="score"
                        required
                        onKeyDown={(e) => {
                          if (e.key === "Enter") {
                            const target = e.target as HTMLInputElement; //neeed as HTML input element beacuse e can be anything and typse need toknow it is input iwth value
                            handleSubmitScore({
                              score: target.value,
                              post_id: post.id,
                            });
                          }
                        }}
                      />
                    </label>
                  </div>
                </div>
                <div className="text">
                  {post.text_content && <p> {post.text_content} </p>}
                </div>

                {post.media_type === "image" && (
                  <div className="media">
                    <img
                      src={
                        "https://bsky.social/xrpc/com.atproto.sync.getBlob?did=" +
                        media_data.did +
                        "&cid=" +
                        media_data.image_link
                      }
                      alt={media_data.alt_text || "Thumb Image"}
                    ></img>
                  </div>
                )}

                {post.media_type === "external" && media_data && (
                  <div className="article">
                    <a
                      href={media_data.uri}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <img
                        src={
                          "https://bsky.social/xrpc/com.atproto.sync.getBlob?did=" +
                          media_data.did +
                          "&cid=" +
                          media_data.thumb
                        }
                        alt="thumbnail of website"
                      />
                      <p>{media_data.title}</p>
                      <p>{media_data.description}</p>
                    </a>
                  </div>
                )}

                <div className="meta_data">
                  <p>
                    retweets: {post.repost_count}&nbsp;&nbsp;&nbsp;&nbsp; views:{" "}
                    {post.repost_count}&nbsp;&nbsp;&nbsp;&nbsp; favorites:{" "}
                    {post.like_count}
                  </p>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

function setErrorMessage(arg0: string) {
  throw new Error("Function not implemented.");
}

interface TruncateProps {
  text: String;
}

function TrencateText({ text }: TruncateProps) {
  const words = text.split(" ");
  if (words.length <= 50) {
    return text;
  }

  return words.slice(0, 50).join(" ") + "...";
}
