/**
 * Contract Generation Page
 * - Dropdown to select template
 * - Dynamic form based on template placeholders
 * - Submit to API
 */
import React, { useState, useEffect } from "react";
import DynamicForm from "../components/DynamicForm.jsx";
import { fetchTemplates, fetchPlaceholders, submitContract } from "../api/contracts.js";
import "../styles.css";

function ContractGenerationPage() {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState("");
  const [placeholders, setPlaceholders] = useState(null);
  const [loading, setLoading] = useState(false);
  const [formLoading, setFormLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Fetch available templates on mount
  useEffect(() => {
    const loadTemplates = async () => {
      try {
        setLoading(true);
        const data = await fetchTemplates();
        setTemplates(data.templates || []);
        setError("");
      } catch (err) {
        setError(err.message || "Failed to load templates");
        setTemplates([]);
      } finally {
        setLoading(false);
      }
    };

    loadTemplates();
  }, []);

  // Fetch placeholders when template changes
  useEffect(() => {
    if (!selectedTemplate) {
      setPlaceholders(null);
      return;
    }

    const loadPlaceholders = async () => {
      try {
        setLoading(true);
        const data = await fetchPlaceholders(selectedTemplate);
        setPlaceholders(data);
        setError("");
      } catch (err) {
        setError(err.message || "Failed to load template placeholders");
        setPlaceholders(null);
      } finally {
        setLoading(false);
      }
    };

    loadPlaceholders();
  }, [selectedTemplate]);

  const handleFormSubmit = async (formData) => {
    try {
      setFormLoading(true);
      setError("");
      const result = await submitContract(selectedTemplate, formData);
      setSuccess(`Contract generated successfully! File: ${result.file}`);
      setSelectedTemplate("");
      setPlaceholders(null);
    } catch (err) {
      setError(err.message || "Failed to generate contract");
    } finally {
      setFormLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="card">
        <h2>Generate Contract</h2>

        {/* Template Selection */}
        <div className="form-section">
          <h3>Step 1: Select Template</h3>
          <div className="form-group">
            <label htmlFor="template-select" className="form-label">
              Contract Type
            </label>
            <select
              id="template-select"
              className="form-input"
              value={selectedTemplate}
              onChange={(e) => setSelectedTemplate(e.target.value)}
              disabled={loading}
            >
              <option value="">-- Choose a template --</option>
              {templates.map((template) => (
                <option key={template} value={template}>
                  {template}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Error Message */}
        {error && <div className="alert alert-error">{error}</div>}

        {/* Success Message */}
        {success && <div className="alert alert-success">{success}</div>}

        {/* Dynamic Form */}
        {selectedTemplate && placeholders && !loading && (
          <div className="form-section">
            <h3>Step 2: Fill in Contract Details</h3>
            <DynamicForm
              placeholders={placeholders}
              onSubmit={handleFormSubmit}
              isLoading={formLoading}
            />
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="alert alert-info">Loading template details...</div>
        )}
      </div>
    </div>
  );
}

export default ContractGenerationPage;
