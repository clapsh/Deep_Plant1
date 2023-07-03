import {useState, useEffect} from "react";
import styles from "./Search.module.css";
import {FaMagnifyingGlass ,FaCalendarDays, FaAngleDown} from "react-icons/fa6";
import DatePicker from "react-datepicker";
import { ko } from 'date-fns/esm/locale';
import "react-datepicker/dist/react-datepicker.css";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

function Search(){
    const [search, setSearch] = useState("");
    // 날짜기반 검색인지 아닌지 확인 
    const [isDate, setIsDate] = useState(false);
    const [date, setDate] = useState(new Date());
    //select value set
    const [value, setValue] = useState('user_based');
    const [toggle , setToggle] = useState(false);

    const onChange = (e) => {
        setSearch(e.target.value)
        console.log(e.target.value)
    }
    

    const handleChange = (event) => {
        setCategoryItem(event.target);
        event.target.value === "date_based" ? setIsDate(true) : setIsDate(false);
        setValue(event.target.value);
           // api 호출 
    };
    const category = [
        {
            name:"사용자 검색",
            value:"user_based"
        },
        {
            name:"날짜 검색",
            value:"date_based"
        }
    ];
    const [categoryItem, setCategoryItem] = useState(category[0]);
    
    function filterCategory (category){
        setCategoryItem(category);
        setToggle(false);
        category.value === "date_based" ? setIsDate(true) : setIsDate(false);
        // api 호출 
    }
    /*
  <div className="MuiSelect-select">
                    <div className={`${styles.search_toggle} ${toggle? styles.open : ''}`}
                        onClick={()=>setToggle(!toggle)}
                    >
                        {categoryItem.name}
                        <FaAngleDown/>
                    </div>
                    
                    {console.log(toggle)}

                    {toggle && (
                        <div className={styles.search_toggle_box}>
                            {category.map((c, idx )=>
                                (<div className={styles.search_toggle_box_item} key={idx} onClick={()=> filterCategory(c)}>
                                    {c.name}
                                </div>)
                            )}
                        </div>
                    )}
                </div>
    */
    return(
        <div>
            <div className={ ` ${styles.search}`}>
                <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel id="demo-simple-select-standard-label">검색</InputLabel>
                    <Select
                    labelId="demo-simple-select-standard-label"
                    id="demo-simple-select-standard"
                    value={value}
                    onChange={handleChange}
                    label="검색 설정"
                    >
                    <MenuItem value="user_based" onClick={()=> filterCategory(category[0])}>
                        사용자 검색
                    </MenuItem>
                    <MenuItem value="date_based" onClick={()=> filterCategory(category[1])}>날짜 검색</MenuItem>
                    </Select>
                </FormControl>
                
                
                <div className={styles.search_input}>
                    {isDate ?
                        (<DatePicker className={styles.search_input_date}  dateFormat="yyyy년 MM월 dd일" locale={ko} selected={date} onChange={date => setDate(date)} />) 
                    : (<TextField  fullWidth
                        id="filled-search"
                        label="Search field"
                        type="search"
                        variant="filled"
                        onChange={onChange}
                        value={search} 
                      />
                        )
                    }
                   <div className={styles.search_btn_wrapper}>
                    <button className={styles.search_btn} onClick={()=>{console.log('click button')}}>
                        <FaMagnifyingGlass onClick={()=>{console.log('clicked')}}/>
                        </button>
                   </div>
                  
                </div>
            </div>
        </div>
    );
}

export default Search;
