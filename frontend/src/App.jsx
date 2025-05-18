import { useState, useEffect } from "react";
import AuthPage from './pages/AuthPage';
import CustomerRouter from "./routers/CustomerRouter";
import CouriorRouter from "./routers/CouriorRouter";
import VendorRouter from "./routers/VendorRouter";
import './styles.css';
function App() {
  const [user, setUser] = useState(null);

  const handleUserLogin = (userData) => {
    setUser(userData);
    console.log('用戶已登入:', userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  // 當用戶未登入時，顯示認證頁面
  if (!user) {
    return <AuthPage onUserAuthenticated={handleUserLogin} />;
  }

  // 用戶已登入後的內容
  return (
    <>
      {user.user_type === 'customer' && (
          <CustomerRouter user={user} handleLogout={handleLogout}/>
      )}
      {user.user_type === 'courier' && (
          <CouriorRouter user={user} handleLogout={handleLogout}/>
      )}
      {user.user_type === 'vendor' && (
          <VendorRouter user={user} handleLogout={handleLogout}/>
      )}
    </>
        // {user.user_type === 'courier' && (
        //   <div className="courier-dashboard">
        //     <h2>快遞員主頁</h2>
        //     <p>評分: {user.profile?.rating || '0'}</p>
        //     <p>車輛類型: {user.profile?.vehicle_type || '未設定'}</p>
        //     <p>車牌號碼: {user.profile?.license_plate || '未設定'}</p>
            
        //   </div>
        // )}
        
        // {user.user_type === 'vendor' && (
        //   <div className="vendor-dashboard">
        //     <h2>廠商主頁</h2>
            
        //   </div>
        // )}
  );
}

export default App;