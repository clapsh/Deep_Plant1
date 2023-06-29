import {useState, useEffect} from "react"
import Meat from "./Meat";

function DataLoad(){
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [items, setItems] = useState({});

    const getData = async() => {
        const json = await(
            await fetch(
                '/meat'
               // `https://yts.mx/api/v2/list_movies.json?minimum_rating=9&sort_by=year`
                )
        ).json();
        setItems(json.data.movies);
        setIsLoaded(true);
        /*const response = await (fetch('/meat').catch(handleError));
        if (response.ok){
            const json = await(response).json();
            setItems(json);
            setIsLoaded(true);
        } else{
            // error 
            setIsLoaded(true);
            setError();
            return Promise.reject(response);
        }*/
        /*
        await fetch(`https://yts.mx/api/v2/list_movies.json?minimum_rating=9&sort_by=year`).then((response) => {
            // 네트워크 에러가 난 경우
            if (response.status >= 400 && response.status < 600) {
              throw new Error("Bad response from server");
            }
            return response;
        }).then((returnedResponse) => {
           // response객체가 성공적으로 반환 된 경우
           console.log('success');
           console.log(returnedResponse.data)
           const json = (returnedResponse.data.json());
           setItems(json);
            setIsLoaded(true);
        }).catch((error) => {
          // 에러가 발생한 경우
          console.warn(error);
          setIsLoaded(true);
          setError(error);
        });*/
        
    }
    
    useEffect(()=>{
        getData();
    },[]);


    //fetch 확인
    console.log(items);
    if (error){
        return <>{error.message}</>
    }

    return (
        <div>
            {
            isLoaded 
            ? <div> 
                {items.map((item) =>
                <Meat/>                
                )}
            </div>
            : <div> <span>Loading...</span> </div>
            }

           
        </div>
    );

}

export default DataLoad;