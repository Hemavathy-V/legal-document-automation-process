/**
 * Templates feature: table of contract templates.
 */
import React, { useState } from "react";
import TemplateModal from "./TemplateModal.jsx";

function TemplatesTable({ templates, token }) {
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleViewClick = (template) => {
    setSelectedTemplate(template);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedTemplate(null);
  };

  if (!templates || templates.length === 0) {
    return <p>No templates found.</p>;
  }

  return (
    <>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Template Name</th>
              <th>Type</th>
              <th>File Path</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {templates.map((t) => (
              <tr key={t.id}>
                <td>{t.id}</td>
                <td>{t.template_name}</td>
                <td>{t.template_type}</td>
                <td>{t.file_path}</td>
                <td>
                  <button
                    className="btn btn-small btn-primary"
                    onClick={() => handleViewClick(t)}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {isModalOpen && (
        <TemplateModal template={selectedTemplate} token={token} onClose={handleCloseModal} />
      )}
    </>
  );
}

export default TemplatesTable;
