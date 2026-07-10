const API = "http://localhost:8000";

// ── Helpers ───────────────────────────────────────────────────────────────────

function getToken() {
  return sessionStorage.getItem("access_token");
}

function setToken(token) {
  sessionStorage.setItem("access_token", token);
}

function clearToken() {
  sessionStorage.removeItem("access_token");
}

function showAlert(id, message, type = "error") {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = message;
  el.className = `alert${type === "success" ? " success" : ""}`;
}

function hideAlert(id) {
  const el = document.getElementById(id);
  if (el) el.className = "alert hidden";
}

function setLoading(btnId, spinnerId, loading) {
  const btn = document.getElementById(btnId);
  const sp  = document.getElementById(spinnerId);
  if (!btn || !sp) return;
  btn.disabled = loading;
  sp.classList.toggle("hidden", !loading);
}

// ── Tab switching ─────────────────────────────────────────────────────────────

function switchTab(tab) {
  const isLogin = tab === "login";
  document.getElementById("form-login").classList.toggle("hidden", !isLogin);
  document.getElementById("form-register").classList.toggle("hidden", isLogin);
  document.getElementById("tab-login").classList.toggle("active", isLogin);
  document.getElementById("tab-register").classList.toggle("active", !isLogin);
  hideAlert("login-alert");
  hideAlert("register-alert");
}

// ── Auth handlers ─────────────────────────────────────────────────────────────

async function handleLogin(e) {
  e.preventDefault();
  hideAlert("login-alert");
  setLoading("login-btn", "login-spinner", true);

  const email    = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;

  try {
    const res = await fetch(`${API}/login`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      showAlert("login-alert", data.detail || "Login failed");
      return;
    }

    setToken(data.access_token);
    window.location.href = "dashboard.html";
  } catch {
    showAlert("login-alert", "Cannot reach the server. Is the backend running?");
  } finally {
    setLoading("login-btn", "login-spinner", false);
  }
}

async function handleRegister(e) {
  e.preventDefault();
  hideAlert("register-alert");
  setLoading("register-btn", "register-spinner", true);

  const email    = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value;

  try {
    const res = await fetch(`${API}/register`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      showAlert("register-alert", data.detail || "Registration failed");
      return;
    }

    showAlert("register-alert", "Account created — you can now log in.", "success");
    setTimeout(() => switchTab("login"), 1200);
  } catch {
    showAlert("register-alert", "Cannot reach the server. Is the backend running?");
  } finally {
    setLoading("register-btn", "register-spinner", false);
  }
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

async function loadDashboard() {
  const token = getToken();
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  try {
    const res = await fetch(`${API}/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      clearToken();
      window.location.href = "index.html";
      return;
    }

    const user = await res.json();
    document.getElementById("user-email").textContent   = user.email;
    document.getElementById("user-id").textContent      = `#${user.id}`;
    document.getElementById("user-created").textContent = new Date(user.created_at).toLocaleString();
  } catch {
    document.getElementById("user-email").textContent = "Error loading user data";
  }
}

function logout() {
  clearToken();
  window.location.href = "index.html";
}

// ── Route guard ───────────────────────────────────────────────────────────────

(function init() {
  const page = window.location.pathname;

  if (page.endsWith("dashboard.html")) {
    loadDashboard();
  } else {
    // Redirect already-logged-in users away from the auth page
    if (getToken()) {
      window.location.href = "dashboard.html";
    }
  }
})();
