/**
 * Template Modal: displays template content in a popup
 */
import React, { useState, useEffect } from "react";
import { fetchTemplateContent } from "../../api/templates.js";

function TemplateModal({ template, token, onClose }) {
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!template || !token) return;

    const loadContent = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await fetchTemplateContent(template.template_name, token);
        setContent(data.content);
      } catch (err) {
        setError(err.message || "Failed to load template content");
      } finally {
        setLoading(false);
      }
    };

    loadContent();
  }, [template, token]);

  if (!template) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{template.template_name}</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        <div className="modal-body">
          {loading && <div className="loading">Loading template content...</div>}
          {error && <div className="modal-error">{error}</div>}
          {content && (
            <div 
              className="template-content"
              dangerouslySetInnerHTML={{ __html: content }}
            />
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default TemplateModal;
