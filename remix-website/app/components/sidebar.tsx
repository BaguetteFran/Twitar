import { Fragment, useState, useContext} from 'react';
import { Link } from "@remix-run/react";
import MainListButton, { ChildListButton } from './buttons';
import { useSidebar } from '~/components/SidebarContext';
import 'app/css/sidebar.css'





/* ----------------------------------------------------------------- */

interface SidebarProps {
    setActiveTopic: (topic: string) => void;  // `setActiveTopic` takes a string and returns void
  }

export default function Sidebar({setActiveTopic}: SidebarProps) { 
    
    const [isDropdownVisible, setIsDropdownVisible] = useState(false);
    const { isSidebarOpen, setIsSidebarOpen } = useSidebar();


    const toggleSidebar = () => { 
        setIsSidebarOpen(!isSidebarOpen);
    }
    const toggleDropdown = () => {
      setIsDropdownVisible(!isDropdownVisible);
    };
  
    
    return (
        <Fragment>
            <div className={`sidebar ${isSidebarOpen ? 'sidebar--open' : 'sidebar--close'}`}>
            <button onClick={toggleSidebar}> {isSidebarOpen ? 'close' : 'expand'} </button>
            {isSidebarOpen && (
                <div className='spacer'>
                <ul className="sidebar_elements">
                    <MainListButton onClick={toggleDropdown} topic='Topics' drop={true} arrow={isDropdownVisible}>

                    <div className={`dropdown ${isDropdownVisible ? 'dropdown--open' : 'dropdown--close'}`}>
                        <ul className='dropdown_list'>
                            <ChildListButton topic='Science'></ChildListButton>
                            <ChildListButton topic='Math'></ChildListButton>
                            <ChildListButton topic='Stocks'></ChildListButton>
                            <ChildListButton topic='Chemistry'></ChildListButton>
                        </ul>
                    </div>   
                    
                    </MainListButton>
        
                    <MainListButton topic='Profile'></MainListButton>
                    <MainListButton topic='Users'></MainListButton>
                    <MainListButton topic='Settings'></MainListButton>

                </ul>
                </div>
            )}
            </div>
        
        </Fragment>
    );
  };
  


