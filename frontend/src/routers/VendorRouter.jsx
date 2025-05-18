import { BrowserRouter, Routes, Route, NavLink  } from "react-router-dom";
import HeaderBar from '../components/HeaderBar';
import VendorHomePage from '../pages/vendor/VendorHomePage';
import ReviseMenuPage from "../pages/vendor/ReviseMenuPage";

function VendorRouter({user, handleLogout}) {
  return (
    <BrowserRouter>
      <div className="app-container">
        <HeaderBar user={user} handleLogout={handleLogout}>
          <nav>
            <NavLink to="/" className={({ isActive }) => isActive ? "active" : ""}>首頁</NavLink>
            <NavLink to="/menu/revise" className={({ isActive }) => isActive ? "active" : ""}>修改餐點</NavLink>
          </nav>
        </HeaderBar>
        
        <main>
          <Routes>
            <Route path="/" element={<VendorHomePage user={user} />} />
            <Route path="/menu/revise" element={<ReviseMenuPage user={user} />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default VendorRouter;