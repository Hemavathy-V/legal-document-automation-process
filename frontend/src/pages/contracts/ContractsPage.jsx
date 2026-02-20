/**
 * Contracts page: list contracts with status and jurisdiction filters.
 */
import React, { useMemo, useState } from "react";
import { fetchContracts } from "../../api/contracts.js";
import ContractsTable from "./ContractsTable.jsx";

function ContractsPage({ token }) {
  const [contracts, setContracts] = useState([]);
  const [statusFilter, setStatusFilter] = useState("all");
  const [jurisdictionFilter, setJurisdictionFilter] = useState("all");
  const [loaded, setLoaded] = useState(false);

  React.useEffect(() => {
    if (!token) return;
    fetchContracts(token)
      .then(setContracts)
      .catch(() => setContracts([]))
      .finally(() => setLoaded(true));
  }, [token]);

  const filteredContracts = useMemo(() => {
    return contracts.filter((c) => {
      const statusOk =
        statusFilter === "all" || c.status.toLowerCase() === statusFilter.toLowerCase();
      const jurisdictionOk =
        jurisdictionFilter === "all" ||
        c.jurisdiction.toLowerCase() === jurisdictionFilter.toLowerCase();
      return statusOk && jurisdictionOk;
    });
  }, [contracts, statusFilter, jurisdictionFilter]);

  const statusOptions = useMemo(
    () => [...new Set(contracts.map((c) => c.status))],
    [contracts]
  );
  const jurisdictionOptions = useMemo(
    () => [...new Set(contracts.map((c) => c.jurisdiction))],
    [contracts]
  );

  return (
    <section className="contracts-page">
      <h2>Contracts</h2>
      <div className="filters">
        <div className="field">
          <span>Status</span>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All</option>
            {statusOptions.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <span>Jurisdiction</span>
          <select
            value={jurisdictionFilter}
            onChange={(e) => setJurisdictionFilter(e.target.value)}
          >
            <option value="all">All</option>
            {jurisdictionOptions.map((j) => (
              <option key={j} value={j}>
                {j}
              </option>
            ))}
          </select>
        </div>
      </div>
      {loaded && <ContractsTable contracts={filteredContracts} />}
    </section>
  );
}

export default ContractsPage;
