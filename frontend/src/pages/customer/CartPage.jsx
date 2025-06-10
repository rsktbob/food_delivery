import React, { useState, useEffect } from 'react';
import { useParams,useNavigate } from 'react-router-dom';
import { updateCartItemQuantity, deleteCartItem, fetchCart } from '../../api';
import CartItem from '../../components/CartItem';
import OrderForm from './OrderForm'

function CartPage({userId}){
    const [cart, setCart] = useState(
        {
            id:"",
            items: [],
            total_price: 0
        }
    );
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        fetchCart()
            .then(data => {
                setCart(data);
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

    const handleCartItemUpdate = (cartItemId, quantity) => {
        updateCartItemQuantity(cartItemId, quantity)
        .then(response => {
            setRefresh(prev => !prev);
        })
        .catch(err => console.log("增加食物失敗:", err));
    }

    const navigate = useNavigate();
    const handleClick = () => {
        navigate(`/order`);
    };


    return (
        <div>
            <h2>我的購物車</h2>
            <hr className="my-4" style={{ borderTop: '2px solid #333' }} />
            {/* 顯示購物車中的餐點 */}
            <div className="mt-4">
                <div className="row">
                    {cart.items.map(item => (
                        <div key={item.id} className="col-md-4 mb-3">
                            <CartItem cartItem={item} onQuantityUpdate={handleCartItemUpdate} onRemove={handleCartItemDelete}></CartItem>
                        </div>
                    ))}
                </div>
            </div>
            
            <button className="btn btn-primary position-fixed" onClick={handleClick}>
                結帳
            </button>

        </div>
    )
}

export default CartPage