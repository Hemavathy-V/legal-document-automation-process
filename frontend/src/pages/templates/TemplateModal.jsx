/**
 * Template Modal: displays template content in a popup
 */
import React, { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import { fetchTemplateContent } from "../../api/templates.js";

function TemplateModal({ template, token, onClose }) {
  const [content, setContent] = useState("");
  const [contentFormat, setContentFormat] = useState("html");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!template || !token) return;

    const loadContent = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await fetchTemplateContent(template.template_name, token);
        setContent(data.content || "");
        setContentFormat(data.format || "text");
      } catch (err) {
        setError(err.message || "Failed to load template content");
      } finally {
        setLoading(false);
      }
    };

    loadContent();
  }, [template, token]);

  useEffect(() => {
    if (!template) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const onKeyDown = (event) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [template, onClose]);

  if (!template) return null;

  const frameDocument = `<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      :root { color-scheme: light; }
      body {
        margin: 0;
        padding: 2rem;
        color: #1e293b;
        background: #ffffff;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.8;
      }
      .document-view { font-size: 1rem; }
      .document-view p { margin: 0.8rem 0; white-space: pre-wrap; }
      .document-view h1,
      .document-view h2,
      .document-view h3,
      .document-view h4,
      .document-view h5,
      .document-view h6 {
        margin: 1.5rem 0 0.8rem 0;
        font-weight: 600;
        color: #0f172a;
      }
      .document-view h1 {
        font-size: 1.8rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
      }
      .document-view h2 { font-size: 1.4rem; margin-top: 1.8rem; }
      .document-view h3 { font-size: 1.1rem; }
      .document-view strong { font-weight: 700; }
      .document-view em { font-style: italic; }
      .document-view u { text-decoration: underline; }
      .document-view ul,
      .document-view ol { margin: 0.6rem 0 0.6rem 1.5rem; }
      .document-view li { margin-bottom: 0.5rem; }
      .document-view li::marker { color: #64748b; }
    </style>
  </head>
  <body>${content}</body>
</html>`;

  const modal = (
    <div
      className="modal-overlay"
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0, 0, 0, 0.72)",
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        padding: "2vh 2vw",
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        className="modal-content modal-large"
        role="dialog"
        aria-modal="true"
        aria-label={`${template.template_name} preview`}
        style={{
          position: "fixed",
          top: "6vh",
          left: "50%",
          transform: "translateX(-50%)",
          width: "min(980px, 88vw)",
          maxWidth: "980px",
          borderRadius: "16px",
          overflow: "hidden",
          zIndex: 1001,
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h2>{template.template_name}</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        <div className="modal-body modal-body--viewer">
          {loading && <div className="loading">Loading template content...</div>}
          {error && <div className="modal-error">{error}</div>}
          {!loading && !error && content && contentFormat === "html" && (
            <iframe
              className="template-frame"
              title={`${template.template_name} content`}
              srcDoc={frameDocument}
              style={{ width: "100%", minHeight: "68vh", border: "none", borderRadius: "10px" }}
            />
          )}
          {!loading && !error && content && contentFormat !== "html" && (
            <pre className="template-plain-text">{content}</pre>
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

  return createPortal(modal, document.body);
}

export default TemplateModal;
