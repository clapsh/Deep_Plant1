import PropTypes from "prop-types";
import styles from "./Meat.module.css";
import {FaRegPenToSquare} from "react-icons/fa6";
import MeatTab from "./MeatTab";
import meatImg from "../src_assets/meat.jpeg"
// 고기 데이터를 받아서 조회/수정 
function Meat({id, butcheryPlaceNm, butcheryYmd, deepAging, email, farmAddr, fresh, gradeNm,
    heated, l_division, lab_data , s_division, saveTime, species, tongue, traceNumber}){
    // API관련 데이터 JSON으로 변환
    const apiData = {
      "butcheryPlaceNm" : {butcheryPlaceNm},
      "butcheryYmd" : {butcheryYmd},
      "farmAddr" : {farmAddr},
      "gradeNm" : {gradeNm},
      "l_division": {l_division},
      "s_division" : {s_division},
      "species" : {species},
      "traceNumber" : {traceNumber},
    };
   // const apiData = JSON.stringify(apiDataToJSON)
    console.log('Meats');
    return (
    <div className={styles.meat}>
        <div className={styles.meat_info}>
            <div className={styles.meat_code}>
                <span>{id}</span>
                <FaRegPenToSquare/>
            <div>
            <div>
              {email}
            </div>
            <div>
              {saveTime}
            </div>
            
          </div>

            </div>
            <div className={styles.meat_img}>
                <img src={meatImg}/>
            </div>
        </div>
        <MeatTab
          fresh={fresh}
          heated={heated}
          lab_data={lab_data}
          tongue={tongue}
          apiData = {apiData}
        />
        
    </div>);
}

Meat.propTypes={
    id: PropTypes.string.isRequired,
    butcheryPlaceNm: PropTypes.string.isRequired ,
    butcheryYmd: PropTypes.string.isRequired, 
    deepAging: PropTypes.arrayOf(PropTypes.string), 
    email: PropTypes.string.isRequired, 
    farmAddr: PropTypes.string.isRequired, 
    fresh: PropTypes.shape({
        marbling: PropTypes.number,
        color:  PropTypes.number,
        texture:  PropTypes.number,
        surfaceMoisture: PropTypes.number,
        total: PropTypes.number,
      }), 
    gradeNm: PropTypes.string.isRequired,
    heated: PropTypes.shape({
        flavor: PropTypes.number,
        juiciness:  PropTypes.number,
        tenderness:  PropTypes.number,
        umami: PropTypes.number,
        palability: PropTypes.number,
      }), 
    l_division: PropTypes.string.isRequired,
    lab_data: PropTypes.shape({
        L: PropTypes.number,
        a:  PropTypes.number,
        b:  PropTypes.number,
        DL: PropTypes.number,
        CL: PropTypes.number,
        RW: PropTypes.number,
        ph:  PropTypes.number,
        WBSF:  PropTypes.number,
        Cardepsin_activity: PropTypes.number,
        MFI: PropTypes.number,
      }), 
    s_division: PropTypes.string.isRequired, 
    saveTime: PropTypes.string.isRequired, 
    species: PropTypes.string.isRequired, 
    tongue: PropTypes.shape({
        sourness: PropTypes.number,
        bitterness:  PropTypes.number,
        umami: PropTypes.number,
        richness: PropTypes.number,
      }), 
    traceNumber: PropTypes.string.isRequired,

}

export default Meat;