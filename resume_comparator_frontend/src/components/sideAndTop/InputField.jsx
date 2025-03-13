import React from "react"; // Import React
const InputField = ({
  label,
  name,
  type = "text",
  value,
  options,
  onChange,
  readOnly = false,
  placeholder = "",
}) => {
  return (
    <div className="mb-3">
      <label className="form-label">{label}</label>
      {type === "select" ? (
        <select
          name={name}
          className="form-select"
          value={value}
          onChange={onChange}
          disabled={readOnly} // Disabled select when readOnly is true
          required
        >
          {options?.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          name={name}
          className="form-control"
          value={value}
          onChange={onChange}
          readOnly={readOnly} // Readonly applied only for input types
          required
          placeholder={placeholder}
        />
      )}
    </div>
  );
};

export default InputField;