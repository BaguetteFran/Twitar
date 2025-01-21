import { Fragment, useEffect, useRef, useState} from 'react';
import { Tweet } from "app/interfaces/tweet_interface"
import "app/css/topic_div.css"
import '/app/css/global-styles.css'


interface TweetDataProps { 
    data: Tweet[]
}

interface PostProps { 
    tweet: Tweet;
}








export default function TweetStream({data}: TweetDataProps){ 

   

    const [openPost, setOpenPost] = useState<Map<string, boolean>>(new Map());
    const postRef = useRef<Map<string, HTMLLIElement>>(new Map());
    

    const togglePost = (id : string) => { 

        console.log("been clicked big ")

        setOpenPost((prev) => { 
            const newState = new Map(prev);
            const isOpen = newState.get(id) || false;
            newState.set(id, !isOpen);
            return newState;
        });

        const postElement = postRef.current.get(id);
        if (postElement != undefined) { 
            postElement.scrollIntoView({ 
                behavior: 'smooth', 
            })
        }

    }


    
    return ( 
        <div className="segment-container">

        

            <ul> 
                
                {data.slice(0, 20).map((tweet) => ( 
                
                    <li key={tweet.id} 
                        ref={(el) => {
                            if (el) { 
                                postRef.current.set(tweet.id, el);  
                            } else { 
                                postRef.current.delete(tweet.id)
                            }

                    }}>
                            
                            <Post tweet={tweet} open_stat={!!openPost.get(tweet.id)} onClick={() => togglePost({ id: tweet.id })} />

                    </li>
                ))}
                    
            </ul> 
        </div>       
    );
};





function Post({
    tweet,
    open_stat,
    onClick,
  }: {
    tweet: Tweet;
    open_stat: boolean;
    onClick: () => void;
  }) { 



  return ( 

        <div className={`post-main ${open_stat ? 'post-main--open' : 'post-main--closed'}`} onClick={onClick}>
            {!open_stat ? (
                <div className="left-right" >

                

                    <div className="left-closed">
                        <div className="profile">
                            <div className="profile-img-containter">
                                {tweet.profile_img && 
                                    <img src={tweet.profile_img} alt="" className="profile-img" />
                                }
                            </div>
                            <div className="profile-info">
                                <h1>{tweet.screen_name}</h1>
                                <p>helloo this is ya boi</p>
                            </div>
                        </div>
                            

                        <div className="content">


                            <div className="content-info">
                                <div className="headline">
                                    
                                {tweet.text && 
                                    <p> <b>{TruncateText(tweet.text)}</b> </p>
                                }
                                    
                                </div>
                                <div className="post-meta">

                                </div>

                            </div>
                        </div>

                    </div> 

                    <div className="content-img-container">
                        {tweet.media &&
                            <img src={tweet.media} alt="post-img" className='content-img'></img>
                        }
                    </div>
                    <div className="content-img-container">
                        {tweet.thumbnail && 
                            <Fragment>

                                <img src={tweet.thumbnail} className='content-img' alt="boke"/>
                            
                            </Fragment>
                        }
                    </div>
                </div>
            
            ) : ( 

                <Fragment>
                    <div className="post-open-main">

                        <div className="profile">
                            <div className="profile-img-containter">
                                {tweet.profile_img && (
                                    <img src={tweet.profile_img} alt="" className="profile-img" />
                                )}                                    
                            </div>
                            <div className="profile-info">
                                <h1>{tweet.screen_name}</h1>
                                <p>helloo this is ya boi</p>
                            </div>
                        </div>


                        <div className="img-container-open">
                            {tweet.media && ( 
                                <img src={tweet.media} alt="content image" className="content-img" />
                            )}
                        </div>
                    
                        <div className="open-content-bufer ">
                            <div className="open-content">
                                {tweet.text && ( 
                                    <p>{tweet.text}</p>
                                )}
                            </div>
                        </div> 

                    </div>
                    <div className="post-open-ai">
                        <div className="ai-contianer">
                            hi
                        </div>
                    </div>
                </Fragment> 
                )}
            </div>

    );
}




function TruncateText(text: String) { 

const words = text.split(' ');
if (words.length <= 50) { 
    return text;
}

return words.slice(0, 50).join(" ") + "...";
};
























