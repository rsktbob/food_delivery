function RadioButtonGroup({ options, selectedValue, onChange }) {
  return (
    <div className="user-type-selector">
      {options.map((option) => (
        <label key={option.value}>
          <input
            type="radio"
            name="user_type"
            value={option.value}
            checked={selectedValue === option.value}
            onChange={onChange}
          />
          {option.label}
        </label>
      ))}
    </div>
  );    
}

export default RadioButtonGroup;