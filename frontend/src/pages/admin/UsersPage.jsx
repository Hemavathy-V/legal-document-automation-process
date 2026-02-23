/**
 * Admin — Users page: list all users, create new users, delete users.
 */
import React, { useEffect, useRef, useState } from "react";
import { fetchUsers, createUser, deleteUser } from "../../api/users.js";

const ROLES = ["Lawyer", "Assistant Lawyer", "Admin", "Client"];

const EMPTY_FORM = { user_name: "", email: "", password: "", role: "Lawyer" };

function UsersPage({ token, currentUserId }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");
  const [formSuccess, setFormSuccess] = useState("");
  const [deletingId, setDeletingId] = useState(null);
  const hasFetched = useRef(false);

  const loadUsers = () => {
    setLoading(true);
    fetchUsers(token)
      .then(setUsers)
      .catch(() => setUsers([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!token || hasFetched.current) return;
    hasFetched.current = true;
    loadUsers();
  }, [token]);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setFormError("");
    setFormSuccess("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError("");
    setFormSuccess("");
    setSubmitting(true);
    try {
      await createUser(form, token);
      setFormSuccess(`User "${form.user_name}" created successfully.`);
      setForm(EMPTY_FORM);
      setShowForm(false);
      hasFetched.current = false;
      loadUsers();
    } catch (err) {
      setFormError(err.message || "Failed to create user.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (u) => {
    if (!window.confirm(`Delete user "${u.user_name}" (${u.email})?\nThis action cannot be undone.`))
      return;
    setDeletingId(u.user_id);
    setFormSuccess("");
    setFormError("");
    try {
      await deleteUser(u.user_id, token);
      setFormSuccess(`User "${u.user_name}" deleted successfully.`);
      setUsers((prev) => prev.filter((x) => x.user_id !== u.user_id));
    } catch (err) {
      setFormError(err.message || "Failed to delete user.");
    } finally {
      setDeletingId(null);
    }
  };

  const roleBadgeClass = (role) => {
    const map = {
      Admin: "badge badge--admin",
      Lawyer: "badge badge--lawyer",
      Client: "badge badge--client",
      "Assistant Lawyer": "badge badge--assistant",
    };
    return map[role] || "badge";
  };

  return (
    <section className="users-page">
      <div className="page-header">
        <h2>Users</h2>
        <button
          className="btn-action"
          onClick={() => {
            setShowForm((v) => !v);
            setFormError("");
            setFormSuccess("");
            setForm(EMPTY_FORM);
          }}
        >
          {showForm ? "Cancel" : "+ Add User"}
        </button>
      </div>

      {formSuccess && <p className="alert alert--success">{formSuccess}</p>}
      {formError && !showForm && <p className="alert alert--error">{formError}</p>}

      {showForm && (
        <form className="create-user-form" onSubmit={handleSubmit}>
          <h3>Create New User</h3>
          <div className="form-grid">
            <label className="field">
              <span>Full Name</span>
              <input
                name="user_name"
                type="text"
                value={form.user_name}
                onChange={handleChange}
                placeholder="e.g. Jane Smith"
                required
              />
            </label>
            <label className="field">
              <span>Email</span>
              <input
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="jane@company.com"
                required
              />
            </label>
            <label className="field">
              <span>Password</span>
              <input
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                placeholder="Min 6 characters"
                required
                minLength={6}
              />
            </label>
            <label className="field">
              <span>Role</span>
              <select name="role" value={form.role} onChange={handleChange}>
                {ROLES.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </label>
          </div>
          {formError && <p className="alert alert--error">{formError}</p>}
          <button type="submit" className="btn-action" disabled={submitting}>
            {submitting ? "Creating..." : "Create User"}
          </button>
        </form>
      )}

      {loading ? (
        <p className="loading-text">Loading users...</p>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.user_id}>
                  <td>{u.user_id}</td>
                  <td>{u.user_name}</td>
                  <td>{u.email}</td>
                  <td>
                    <span className={roleBadgeClass(u.role)}>{u.role}</span>
                  </td>
                  <td>
                    {u.user_id !== currentUserId ? (
                      <button
                        className="btn-delete"
                        onClick={() => handleDelete(u)}
                        disabled={deletingId === u.user_id}
                      >
                        {deletingId === u.user_id ? "Deleting…" : "Delete"}
                      </button>
                    ) : (
                      <span className="self-label">You</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {users.length === 0 && <p className="empty-text">No users found.</p>}
        </div>
      )}
    </section>
  );
}

export default UsersPage;
