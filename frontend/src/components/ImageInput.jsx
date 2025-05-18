function ImageInput({ label, id, name, onChange, imagePreview, required=false }) {
  return (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      <input
        type="file"
        id={id}
        name={name}
        accept="image/*"
        onChange={onChange}
        required
      />

      {/* 顯示圖片預覽 */}
      {imagePreview && (
        <div>
          <img
            src={imagePreview}
            alt="Restaurant Preview"
            style={{ width: "200px", height: "auto", marginTop: "10px" }}
          />
        </div>
      )}
    </div>

  )
}

export default ImageInput