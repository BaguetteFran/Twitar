import { Fragment, useState} from 'react';
import '~/css/buttons.css'; 
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons'; // Import the icon you want



interface ButtonProps {
    onClick?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void; 
    topic: React.ReactNode;
    children?: React.ReactNode;
    drop?: boolean;
    arrow?: boolean;
  }



export default function MainListButton({ topic, onClick, children, drop, arrow}: ButtonProps) {
    return (
        <li className='mainlist_li'>
            
            <button className='main_list_button' onClick={onClick ?  onClick : undefined}>
            {topic}
            {drop && (
                <b><div className={`icon ${arrow ? 'icon--open' : 'icon--close'}`}><FontAwesomeIcon icon={faArrowRight} /></div></b>
            )}
            </button> 
            {children && children}

        </li>
         
        

    );
}



export function ChildListButton({  topic, onClick}: ButtonProps) { 

    return ( 
        <li>
            <button className='child_list_button' onClick={onClick ?  onClick : undefined}>
                {topic}
            </button>   
        </li>
    );
}





