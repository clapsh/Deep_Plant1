import React, {useEffect, useRef, useState } from "react";
import styles from "./Sidebar.module.css";
import PropTypes from "prop-types";
import {FaBars ,FaAnglesLeft} from "react-icons/fa6";

//컴포넌트가 사용되는 위치에서 자식요소로 들어가있던 데이터가 {children} 위치로 구현됩니다.
function Sidebar({width = 280, children}){ 
    const [isOpen, setIsOpen] = useState(false);
    const [xPos, setXPos] = useState(width); // 메뉴 토글을 위한 x축 위치 변수 
    const side = useRef();
    //버튼 클릭 시 메뉴 토글 -> xpos가 0일 때 open , width 값일 때 close
    const toggleSide = () =>{
        setXPos(0);
        setIsOpen(true);
    }
    const closeSide = () => {
        setXPos(width);
        setIsOpen(false);
    }
           
    //사이드바 외부 클릭 시 닫힘
    const handleClose  = e => {
        let sideArea = side.current;
        let sideAreaChildren = side.current.contains(e.target);
        // 클릭한 곳이 sideBar/ sideBar의 children이 아니면 닫음
        if (isOpen && (!sideArea || !sideAreaChildren)){
            setXPos(width);
            setIsOpen(false);
        }
    }

    useEffect(()=>{
        window.addEventListener('click', handleClose);
        return ()=>{
            window.removeEventListener('click', handleClose);
        };
    })


    return (
        <div className={styles.container}>
            <div ref={side} className={styles.sidebar} style={{ width: `${width}px`, height: '100%',  transform: `translatex(${-(xPos)}px)`}}>
                    {isOpen
                    ? <button  onClick={() => closeSide() } style={{ transform: `translatex(${width-45}px) translateY(10px)`}} ><FaAnglesLeft onClick={() => closeSide() } /></button> 
                    : <button  onClick={() => toggleSide()} className={styles.button}><FaBars onClick={() => toggleSide()} /></button>
                    }
                    
                
                <div className={styles.content}>{children}</div>
            </div>
        </div>


    );
}

Sidebar.propTypes={
    width: PropTypes.number,
}

export default Sidebar;