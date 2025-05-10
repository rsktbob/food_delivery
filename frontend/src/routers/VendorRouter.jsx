import { BrowserRouter, Routes, Route, NavLink  } from "react-router-dom";
import HeaderBar from '../components/HeaderBar';
import VendorHomePage from '../pages/vendor/VendorHomePage';
import TestPage from '../pages/TestPage';

function VendorRouter({user, handleLogout}) {
  return (
    <BrowserRouter>
      <div className="app-container">
        <HeaderBar user={user} handleLogout={handleLogout}>
          <nav>
            <NavLink to="/" className={({ isActive }) => isActive ? "active" : ""}>首頁</NavLink>
            <NavLink to="/test" className={({ isActive }) => isActive ? "active" : ""}>測試頁面</NavLink>
          </nav>
        </HeaderBar>
        
        <main>
          <Routes>
            <Route path="/" element={<VendorHomePage user={user} />} />
            <Route path="/test" element={<TestPage user={user} />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default VendorRouter;