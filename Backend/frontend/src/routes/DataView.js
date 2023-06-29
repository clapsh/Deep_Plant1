import { useState, useEffect } from "react"
import Base from "../components/Base/BaseCmp";
import DataLoad from "../components/DataLoad";
function DataView(){
    const [loading, setLoading] = useState(true);

    
    return (
        <div>
            <Base/>
            <DataLoad/>
        </div>
    );
}

export default DataView;