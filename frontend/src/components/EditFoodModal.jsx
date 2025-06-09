import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

function EditFoodModal({ show, onClose, onConfirm, food }) {
  const [foodName, setFoodName] = useState('');
  const [price, setPrice] = useState('');
  const [image, setImage] = useState(null); // 新圖檔
  const [previewUrl, setPreviewUrl] = useState(''); // 圖片預覽

  // 載入原始資料
  useEffect(() => {
    if (food) {
      setFoodName(food.name || '');
      setPrice(food.price || '');
      setPreviewUrl(food.image || '');
      setImage(null); // 清除之前上傳的圖片
    }
  }, [food]);

  const handleConfirm = () => {
    if (!foodName.trim() || !price) {
      alert('請填寫名稱與價格');
      return;
    }

    const formData = new FormData();
    formData.append('name', foodName);
    formData.append('price', price);
    if (image) {
      formData.append('image', image); // 僅在有更換時送出新圖
    }

    console.log(food.id);
    onConfirm(food.id, formData); 
  };

  return (
    <Modal show={show} onHide={onClose}>
      <Modal.Header closeButton>
        <Modal.Title>修改食物</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group>
            <Form.Label>食物名稱</Form.Label>
            <Form.Control
              type="text"
              value={foodName}
              onChange={(e) => setFoodName(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mt-3">
            <Form.Label>價格</Form.Label>
            <Form.Control
              type="number"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mt-3">
            <Form.Label>目前圖片</Form.Label>
            {previewUrl && (
              <div className="mb-2">
                <img
                  src={previewUrl}
                  alt="food"
                  style={{ width: '100%', maxHeight: '200px', objectFit: 'cover' }}
                />
              </div>
            )}
            <Form.Control
              type="file"
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files[0];
                setImage(file);
                if (file) {
                  setPreviewUrl(URL.createObjectURL(file));
                }
              }}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onClose}>
          取消
        </Button>
        <Button variant="primary" onClick={handleConfirm}>
          確認修改
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default EditFoodModal;
