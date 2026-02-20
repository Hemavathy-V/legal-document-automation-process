/**
 * Templates page: list contract templates.
 */
import React, { useEffect, useState } from "react";
import { fetchTemplates } from "../../api/templates.js";
import TemplatesTable from "./TemplatesTable.jsx";

function TemplatesPage({ token }) {
  const [templates, setTemplates] = useState([]);

  useEffect(() => {
    if (!token) return;
    fetchTemplates(token)
      .then(setTemplates)
      .catch(() => setTemplates([]));
  }, [token]);

  return (
    <section className="templates-page">
      <h2>Contract Templates</h2>
      <TemplatesTable templates={templates} />
    </section>
  );
}

export default TemplatesPage;
