import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
function DataEdit(){

    const {id} = useParams();
    console.log(id);
}

export default DataEdit;