import { useState, useEffect } from "react";
import AuthPage from './pages/AuthPage';
import './styles.css'; // 假設你會創建這個樣式文件

function App() {
  const [user, setUser] = useState(null);

  const handleUserAuthenticated = (userData) => {
    setUser(userData);
    console.log('用戶已登入:', userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  // 當用戶未登入時，顯示認證頁面
  if (!user) {
    return <AuthPage onUserAuthenticated={handleUserAuthenticated} />;
  }

  // 用戶已登入後的內容
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>{message}</h1>
        <div className="user-info">
          <span>歡迎, {user.username} ({user.user_type})</span>
          <button onClick={handleLogout}>登出</button>
        </div>
      </header>
      
      <main className="app-content">
        {user.user_type === 'customer' && (
          <div className="customer-dashboard">
            <h2>顧客主頁</h2>
            <p>您的地址: {user.profile?.address || '未設定'}</p>
            {/* 這裡可以放置顧客特有的功能 */}
          </div>
        )}
        
        {user.user_type === 'courier' && (
          <div className="courier-dashboard">
            <h2>快遞員主頁</h2>
            <p>評分: {user.profile?.rating || '0'}</p>
            <p>車輛類型: {user.profile?.vehicle_type || '未設定'}</p>
            <p>車牌號碼: {user.profile?.license_plate || '未設定'}</p>
            {/* 這裡可以放置快遞員特有的功能 */}
          </div>
        )}
        
        {user.user_type === 'vendor' && (
          <div className="vendor-dashboard">
            <h2>廠商主頁</h2>
            {/* 這裡可以放置廠商特有的功能 */}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;