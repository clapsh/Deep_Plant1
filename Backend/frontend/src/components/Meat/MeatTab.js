import {useState, useEffect} from "react";
import styles from "./MeatTab.module.css";
import TabBtns from "./TabBtns";
 
//tab 버튼 별 데이터 설정
function MeatTab({fresh, heated , lab_data, tongue, apiData}){
    const [currentTab , setCurrentTab] = useState("");
    const [data, setData] = useState({});
    // 클릭한 tab을 가져오고 tab한 버튼에 따른 데이터를 가져옴 
    const currentTabHandler = (tab)=>{
        fetchDataToTab(tab);
        setCurrentTab(tab);
    }
    /*
    console.log("fresh");
    console.log(fresh);
    console.log( "heated" );
    console.log( heated );
    console.log( "lab_data");
    console.log( lab_data);
    console.log( "tongue");
    console.log( tongue);
    console.log(apiData);
    */
    // tab버튼에 따라서 보여줄 data를 다르게 set함
    const fetchDataToTab =(currentTab)=> {//async(pageNum) =>{\
        switch(currentTab){
            case "firstBtn":
                setData((heated));
                break;
            case "secondBtn":
                setData((fresh));
                break;
            case "thirdBtn":
                setData((tongue));
                break;
            case "fouthBtn":
                setData((lab_data));
                break;
            case "fifthBtn":
                setData((apiData));
                break;
            default:
                setData((null));
                break;
        }
    }

    return(
        <div className={styles.meat_info_container}>
            <TabBtns
                currentTab={currentTab}
                currentTabHandler={currentTabHandler}
            />
            <div className={styles.meat_info_container_content}>
                {console.log('setdata')}
                {data ? JSON.stringify(data) : 'null'}      
            </div>
        </div>
    );
}

export default MeatTab;