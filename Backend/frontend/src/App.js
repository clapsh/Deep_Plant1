import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import Home from "./routes/Home"
import DataView from "./routes/DataView";
import Stats from "./routes/Stats";
import Profile from "./routes/Profile";
import DataEdit from "./routes/DataEdit";
import './App.module.css';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home/>}></Route>
        <Route path="/dataView" element={<DataView/>}></Route>
        <Route path="/stats" element={<Stats/>}></Route>cd 
        <Route path="/profile" element={<Profile/>}></Route>
        <Route path="/dataEdit/:id" element={<DataEdit/>}></Route>
      </Routes>
    </Router>
  );
}

export default App;
stt