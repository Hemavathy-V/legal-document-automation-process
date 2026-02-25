/**
 * Templates page: list contract templates.
 */
import React, { useEffect, useRef, useState } from "react";
import { fetchTemplates } from "../../api/templates.js";
import TemplatesTable from "./TemplatesTable.jsx";

function TemplatesPage({ token }) {
  const [templates, setTemplates] = useState([]);
  const hasFetched = useRef(false);

  useEffect(() => {
    if (!token || hasFetched.current) return;
    hasFetched.current = true;
    
    fetchTemplates(token)
      .then(setTemplates)
      .catch(() => setTemplates([]));
  }, [token]);

  return (
    <section className="templates-page">
      <h2>Contract Templates</h2>
      <TemplatesTable templates={templates} token={token} />
    </section>
  );
}

export default TemplatesPage;
