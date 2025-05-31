import { useState, useEffect } from "react";
import AuthPage from './pages/AuthPage';
import CustomerRouter from "./routers/CustomerRouter";
import CouriorRouter from "./routers/CouriorRouter";
import VendorRouter from "./routers/VendorRouter";
import './styles.css';
import { useNavigate } from 'react-router-dom';

function App() {
  const [user, setUser] = useState(null);
  // 當組件初始化時，檢查是否有存儲在 localStorage 中的用戶資料
  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const navigate = useNavigate();

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
    console.log(userData);
    navigate('/');
    console.log('用戶已登入:', userData);
  };

  const handleLogout = () => {
    setUser(null);
    navigate('/');
    localStorage.removeItem("user");
  };


  // 當用戶未登入時，顯示認證頁面
  if (!user) {
    return <AuthPage onUserAuthenticated={handleLogin} />;
  }
  
  // 用戶已登入後的內容
  return (
    <>
      {user.user_type === 'customer' && <CustomerRouter user={user} handleLogout={handleLogout}/>}
      {user.user_type === 'courier' && <CouriorRouter user={user} handleLogout={handleLogout}/>}
      {user.user_type === 'vendor' && <VendorRouter user={user} handleLogout={handleLogout}/>}
    </>
  );
}

export default App;