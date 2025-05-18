function HeaderBar({user, handleLogout, children}) {
  return (
    <header className="app-header">
        <div className="user-info">
            <span>歡迎, {user.username} {user.user_type === 'customer' ? '(顧客)' : 
                         user.user_type === 'vendor' ? '(商家)' : '(外送員)'}</span>
            <button onClick={handleLogout}>登出</button>
        </div>
        <div className="navigation-container">
            {children}
        </div>
    </header>
  )
}

export default HeaderBar