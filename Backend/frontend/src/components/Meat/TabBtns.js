import styles from "./TabBtns.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
//tab 버튼

const TabBtns= ({
    // MeatTab의 function과 state 전달
    currentTab,
    currentTabHandler,
}) => {
    return (
        <ButtonGroup size="large" aria-label="large button group" className={styles.swithBtn} >
            <Button key="one" className={`${currentTab === "firstBtn" ? styles.tabOn : styles.tabOff} `}
                value="firstBtn"
                onClick={(e)=>{ currentTabHandler(e.target.value);}}>
                가열육
            </Button>
            <Button key="two"  className={`${currentTab === "secondBtn" ? styles.tabOn : styles.tabOff} `}
                    value="secondBtn" 
                    onClick={(e)=>{currentTabHandler(e.target.value);}}>
                신선육
            </Button>
            <Button key="three"  className={`${currentTab === "thirdBtn" ? styles.tabOn : styles.tabOff}  ` }
                    value="thirdBtn"
                    onClick={(e)=>{currentTabHandler(e.target.value);}}  
            >전자혀</Button>
            <Button key="four"className={`${currentTab === "fourthBtn" ? styles.tabOn : styles.tabOff}  `}
                    value="fourthBtn"
                    onClick={(e)=>{currentTabHandler(e.target.value); }} 
            >실험실</Button>
            <Button key="five" className={`${(currentTab === "fifthBtn" ? styles.tabOn : styles.tabOff)}  `}
                    value="fifthBtn"
                    onClick={(e)=>{currentTabHandler(e.target.value); }} 
            >API</Button>
      </ButtonGroup>
        

    )
}

export default TabBtns;