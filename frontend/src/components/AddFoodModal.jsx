import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

function AddFoodModal({ show, onClose, onConfirm, restaurantId }) {
  const [foodName, setFoodName] = useState('');
  const [price, setPrice] = useState('');
  const [image, setImage] = useState(null);

  const handleConfirm = () => {
    if (!foodName.trim() || !price || !image) {
      alert('請填寫所有欄位');
      return;
    }

    const formData = new FormData();
    formData.append('name', foodName);
    formData.append('price', price);
    formData.append('image', image);
    formData.append('restaurant', restaurantId);

    onConfirm(formData);
  };

  return (
    <Modal show={show} onHide={onClose}>
      <Modal.Header closeButton>
        <Modal.Title>新增食物</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group>
            <Form.Label>食物名稱</Form.Label>
            <Form.Control
              type="text"
              placeholder="輸入食物名稱"
              value={foodName}
              onChange={(e) => setFoodName(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mt-3">
            <Form.Label>價格</Form.Label>
            <Form.Control
              type="number"
              placeholder="輸入價格"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mt-3">
            <Form.Label>上傳圖片</Form.Label>
            <Form.Control
              type="file"
              accept="image/*"
              onChange={(e) => setImage(e.target.files[0])}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onClose}>
          關閉
        </Button>
        <Button variant="primary" onClick={handleConfirm}>
          確認新增
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AddFoodModal;
