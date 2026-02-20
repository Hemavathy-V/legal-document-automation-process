/**
 * Contracts feature: table of contracts.
 */
import React from "react";

function ContractsTable({ contracts }) {
  if (!contracts || contracts.length === 0) {
    return <p>No contracts found.</p>;
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Jurisdiction</th>
            <th>Status</th>
            <th>Created By</th>
          </tr>
        </thead>
        <tbody>
          {contracts.map((c) => (
            <tr key={c.contract_id}>
              <td>{c.contract_id}</td>
              <td>{c.contract_type}</td>
              <td>{c.jurisdiction}</td>
              <td>{c.status}</td>
              <td>{c.created_by}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ContractsTable;
