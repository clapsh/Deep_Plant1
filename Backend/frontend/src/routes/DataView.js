import { useState, useEffect } from "react"
import Base from "../components/Base/BaseCmp";
import DataLoad from "../components/DataLoad";
import styles from "./DataView.module.css"
function DataView(){
    const [loading, setLoading] = useState(true);

    
    return (
        <div className={styles.container}>
            <Base/>
            <DataLoad/>
        </div>
    );
}

export default DataView;