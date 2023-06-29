import React from "react";
import {Link} from "react-router-dom";
import styles from './Header.module.css'
import logo from '../../src_assets/deeplant-text-logo.png'
class Header extends React.Component{
    render(){
        return(
            <Link to="/">
            <div className={styles.container}>
                <img className={styles.logo} src={logo}/>
            </div>
            </Link>
            
        );
    }
}

export default Header;