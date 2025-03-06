import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NavBar from './Components/Navbar/navbar';
import Login from './Components/Authentication/login';
import Signup from './Components/Authentication/signup';
import 'bootstrap/dist/css/bootstrap.min.css';
import Home from './Components/Home/home';

function App() {
  
  return (
    <div className='bg-dark' style={{ height: '100vh' }}>
      <Router>
        <NavBar />

        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/login" element={<><Login /></>} />
          <Route path="/signup" element={<><Signup /></>} />
          {/* <Route path="/verify-user/:key" element={<VerifyUser />} /> */}
          {/* <Route path="/logout" element={<Logout />} /> */}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
