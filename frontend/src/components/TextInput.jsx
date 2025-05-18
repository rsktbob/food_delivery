function TextInput({ label, id, type, value, name, onChange, required=false }) {
  return (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      <input
        type={type}
        id={id}
        value={value}
        name={name}
        onChange={onChange}
        required={required}
      />
    </div>
  )
}

export default TextInput