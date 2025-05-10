function CustomerHomePage({user}){
    return(
        <div className="customer-dashboard">
            <h2>顧客主頁test</h2>
            <p>您的地址: {user.profile?.address || '未設定'}</p>

        </div>
    )
}

export default CustomerHomePage