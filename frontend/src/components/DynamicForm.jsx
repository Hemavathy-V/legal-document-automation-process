/**
 * Dynamic form that renders fields based on template placeholders.
 * Handles simple fields and repeating sections (loops).
 */
import React, { useState } from "react";
import "../styles.css";

function DynamicForm({ placeholders, onSubmit, isLoading }) {
  const { simple_fields, loop_fields } = placeholders;

  // Simple fields: { fieldName: "value" }
  const [simpleData, setSimpleData] = useState(
    simple_fields.reduce((acc, field) => ({ ...acc, [field]: "" }), {})
  );

  // Loop fields: { loopName: [{ field1: "", field2: "" }, ...] }
  const [loopData, setLoopData] = useState(
    Object.keys(loop_fields).reduce((acc, loopName) => {
      acc[loopName] = [{}];
      return acc;
    }, {})
  );

  const handleSimpleChange = (field, value) => {
    setSimpleData((prev) => ({ ...prev, [field]: value }));
  };

  const handleLoopChange = (loopName, index, field, value) => {
    setLoopData((prev) => {
      const updatedRows = [...prev[loopName]];
      if (!updatedRows[index]) updatedRows[index] = {};
      updatedRows[index][field] = value;
      return { ...prev, [loopName]: updatedRows };
    });
  };

  const addLoopRow = (loopName) => {
    setLoopData((prev) => ({
      ...prev,
      [loopName]: [...prev[loopName], {}],
    }));
  };

  const removeLoopRow = (loopName, index) => {
    setLoopData((prev) => ({
      ...prev,
      [loopName]: prev[loopName].filter((_, i) => i !== index),
    }));
  };

  const formatFieldName = (field) => {
    return field
      .replace(/_/g, " ")
      .replace(/\./g, " ")
      .replace(/([a-z])([A-Z])/g, "$1 $2")
      .replace(/^./, (str) => str.toUpperCase());
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Filter empty loop rows
    const cleanedLoopData = Object.keys(loopData).reduce((acc, loopName) => {
      acc[loopName] = loopData[loopName].filter(
        (row) => Object.values(row).some((v) => v)
      );
      return acc;
    }, {});

    // Merge simple + loop data
    const formData = { ...simpleData, ...cleanedLoopData };
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      {/* Simple Fields Section */}
      {simple_fields.length > 0 && (
        <div className="form-section">
          <h3>Basic Information</h3>
          <div className="generate-fields-grid">
            {simple_fields.map((field) => (
              <div key={field} className="form-group generate-field-item">
                <label htmlFor={field} className="form-label">
                  {formatFieldName(field)}
                </label>
                <input
                  id={field}
                  type="text"
                  className="form-input"
                  value={simpleData[field] || ""}
                  onChange={(e) => handleSimpleChange(field, e.target.value)}
                  required
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Loop Fields Section */}
      {Object.keys(loop_fields).length > 0 &&
        Object.entries(loop_fields).map(([loopName, nestedFields]) => (
          <div key={loopName} className="form-section">
            <h3>{formatFieldName(loopName)}</h3>

            {loopData[loopName]?.map((row, index) => (
              <div key={index} className="loop-row">
                <div className="loop-header">
                  <span>Entry {index + 1}</span>
                  {loopData[loopName].length > 1 && (
                    <button
                      type="button"
                      className="btn btn-danger btn-sm"
                      onClick={() => removeLoopRow(loopName, index)}
                    >
                      Remove
                    </button>
                  )}
                </div>

                {nestedFields.map((field) => (
                  <div key={field} className="form-group">
                    <label htmlFor={`${loopName}-${index}-${field}`} className="form-label">
                      {formatFieldName(field)}
                    </label>
                    <input
                      id={`${loopName}-${index}-${field}`}
                      type="text"
                      className="form-input"
                      value={row[field] || ""}
                      onChange={(e) =>
                        handleLoopChange(loopName, index, field, e.target.value)
                      }
                    />
                  </div>
                ))}
              </div>
            ))}

            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => addLoopRow(loopName)}
            >
              + Add {formatFieldName(loopName)}
            </button>
          </div>
        ))}

      {/* Submit Button */}
      <div className="form-actions">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Generate Contract"}
        </button>
      </div>
    </form>
  );
}

export default DynamicForm;
