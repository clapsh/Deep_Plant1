import styles from "./TabBtns.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';
//tab 버튼
const TabBtns= ({
    // MeatTab의 function과 state 전달
    currentTab,
    currentTabHandler,
}) => {
    return (
        <div className={styles.swithBtn } >
            
            <button 
                className={((currentTab === "firstBtn") ? styles.tabOn : styles.tabOff) }
                value="firstBtn"
                onClick={(e)=>{
                    console.log('clicked')
                    console.log(e)
                    currentTabHandler(e.target.value);
                }}    
            >
            가열육
            </button>
            <button 
                className={currentTab === "secondBtn" ? styles.tabOn : styles.tabOff}
                value="secondBtn"
                onClick={(e)=>{
                    currentTabHandler(e.target.value);
                }}    
            >
            신선육
            </button>
            <button 
                className={currentTab === "thirdBtn" ? styles.tabOn : styles.tabOff}
                value="thirdBtn"
                onClick={(e)=>{
                    currentTabHandler(e.target.value);
                }}    
            >
            전자혀
            </button>
            <button 
                className={currentTab === "fourthBtn" ? styles.tabOn : styles.tabOff}
                value="fourthBtn"
                onClick={(e)=>{
                    currentTabHandler(e.target.value);
                }}    
            >
            실험실
            </button>
            <button 
                className={(currentTab === "fifthBtn" ? styles.tabOn : styles.tabOff)}
                value="fifthBtn"
                onClick={(e)=>{
                    currentTabHandler(e.target.value);
                }}    
            >
            API
            </button>
        </div>

    )
}

export default TabBtns;