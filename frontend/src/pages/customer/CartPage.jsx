import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { deleteCartItem, fetchCartItems } from '../../api';
import CartItem from '../../components/CartItem';

function CartPage({userId}){
    const [cartItems, setCartItems] = useState([]);
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        fetchCartItems()
            .then(data => {
                setCartItems(data);
                console.log(data);
            })
            .catch(error => {
                console.error(`error: ${error}`);
            });
    }, [refresh]);
    
    const handleCartItemDelete = (cartItemId) => {
        deleteCartItem(cartItemId)
        .then(response => {
            alert(response);
            setRefresh(prev => !prev);
        })
        .catch(err => console.log("刪除食物失敗:", err));
    }

    return(
        <div className="container py-5">
            <h2>我的購物車</h2>
                <hr className="my-4" style={{ borderTop: '2px solid #333' }} />
                {/* 顯示購物車中的餐點 */}
                <div className="mt-4">
                    {cartItems.length === 0 ? (
                    <p>暫無餐點項目</p>
                    ) : (
                    <div className="row">
                        {cartItems.map(item => (
                        <div key={item.id} className="col-md-4 mb-3">
                            <CartItem cartItem={item} onRemove={handleCartItemDelete}></CartItem>
                        </div>
                        ))}
                    </div>
                    )}
                </div>

        </div>
    )
}

export default CartPage