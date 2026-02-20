/**
 * Templates feature: table of contract templates.
 */
import React from "react";

function TemplatesTable({ templates }) {
  if (!templates || templates.length === 0) {
    return <p>No templates found.</p>;
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Template Name</th>
            <th>Type</th>
            <th>File Path</th>
          </tr>
        </thead>
        <tbody>
          {templates.map((t) => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>{t.template_name}</td>
              <td>{t.template_type}</td>
              <td>{t.file_path}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TemplatesTable;
