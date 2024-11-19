
import { useParams } from "@remix-run/react";
import { Fragment } from "react/jsx-runtime";
import {useSidebar} from "~/components/SidebarContext"
import React, { createContext, useContext, useEffect, useRef, useState } from 'react';
import "~/css/topic_div.css"

interface TopicsProps { 
    setActiveTopic : (topic : string) => void;
}

export default function topics({setActiveTopic}: TopicsProps) { 
    
    const { isSidebarOpen, setIsSidebarOpen } = useSidebar();

    return (    
        <div className='topic'>
            <ScrollHeader></ScrollHeader>
            <TopicDiv></TopicDiv>
            <TopicDiv></TopicDiv>
            <TopicDiv></TopicDiv>
            <TopicDiv></TopicDiv>
            <TopicDiv></TopicDiv>
            <TopicDiv></TopicDiv>
            <TopicDiv></TopicDiv>
            <TopicDiv></TopicDiv>
        </div>
    );
}




export function ScrollHeader() { 
    return (
    <button> Toggle</button>
    );
}






export function TopicDiv() { 

    const [isOpen, setIsOpen] = useState(false);
    const postRef = useRef<HTMLDivElement | null>(null);

    const handleOpen = () => { 
        setIsOpen(!isOpen);
    }
    
    useEffect(() => {
        if (isOpen && postRef.current) {
            // Scroll to the center initially
            postRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
            // Add a small delay to adjust the position
            setTimeout(() => {
                if (postRef.current) {
                    postRef.current.scrollTop += 1000; // Offset adjustment for centering
                }
            }, 400); // Adjust the timeout as needed
        }
    }, [isOpen]);
    
    



    return ( 
        <Fragment>
            <div className={`post-main ${isOpen ? 'post-main--open' : 'post-main--closed'}`} onClick={handleOpen} ref={postRef}>
                {!isOpen ? (
                    <div className="left-right">

                    

                        <div className="left-closed">
                            <div className="profile">
                                <div className="profile-img-containter">
                                    <img src="app/img/elric_profile.jpg" alt="" className="profile-img" />
                                </div>
                                <div className="profile-info">
                                    <h1>BaggueFranc</h1>
                                    <p>Astroboi at the university of phoeniz arizon department of biophysics</p>
                                </div>
                            </div>
                                

                            <div className="content">


                                <div className="content-info">
                                    <div className="headline">
                                        <p> <b>"Challenging Assumptions: Do Personas in LLM Prompts Help or Hinder Performance?"</b> </p>
                                    </div>
                                    <div className="post-meta">

                                    </div>

                                </div>
                            </div>

                        </div> 
                           

                        <div className="content-img-container">
                                <img src="app/img/fake.jpg" alt="content image" className="content-img" />
                        </div>
                    </div>
                
                ) : ( 

                    <Fragment>
                        <div className="post-open-main">

                            <div className="profile">
                                <div className="profile-img-containter">
                                    <img src="app/img/elric_profile.jpg" alt="" className="profile-img" />
                                </div>
                                <div className="profile-info">
                                    <h1>BaggueFranc</h1>
                                    <p>Astroboi at the university of phoeniz arizon department of biophysics</p>
                                </div>
                            </div>


                            <div className="img-container-open">
                                    <img src="app/img/fake.jpg" alt="content image" className="content-img" />
                            </div>
                        
                            <div className="open-content-bufer ">
                                <div className="open-content">
                                    <p> 
                                        TCellular viral evasion proteins are specialized molecules produced by viruses to interfere with host cellular mechanisms, allowing the virus to avoid detection and destruction by the host immune system. These proteins play a crucial role in viral pathogenesis, as they enable the virus to persist, replicate, and spread within the host. Viral evasion proteins can target various stages of the immune response, from innate immunity to adaptive immunity. For example, some evasion proteins inhibit the production or signaling of interferons, which are key cytokines that trigger antiviral responses in host cells. Others may inhibit antigen presentation by MHC molecules, preventing infected cells from being recognized by cytotoxic T cells. Some viral proteins even mimic host proteins to avoid immune detection or create decoy molecules that bind to immune receptors, disrupting normal immune function. The strategic production of these evasion proteins allows viruses to establish prolonged infections, contributing to chronic diseases or enhancing their ability to spread within populations. Understanding how viral evasion proteins interact with host immune pathways is critical for developing effective antiviral therapies and vaccines.TCellular viral evasion proteins are specialized molecules produced by viruses to interfere with host cellular mechanisms, allowing the virus to avoid detection and destruction by the host immune system. These proteins play a crucial role in viral pathogenesis, as they enable the virus to persist, replicate, and spread within the host. Viral evasion proteins can target various stages of the immune response, from innate immunity to adaptive immunity. For example, some evasion proteins inhibit the production or signaling of interferons, which are key cytokines that trigger antiviral responses in host cells. Others may inhibit antigen presentation by MHC molecules, preventing infected cells from being recognized by cytotoxic T cells. Some viral proteins even mimic host proteins to avoid immune detection or create decoy molecules that bind to immune receptors, disrupting normal immune function. The strategic production of these evasion proteins allows viruses to establish prolonged infections, contributing to chronic diseases or enhancing their ability to spread within populations. Understanding how viral evasion proteins interact with host immune pathways is critical for developing effective antiviral therapies and vaccines.
                                    </p>
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

       <hr></hr>
        

       </Fragment>


    );

}


























