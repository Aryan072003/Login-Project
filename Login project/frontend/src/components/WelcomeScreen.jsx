import Logo from "../assets/jms-logo.webp";

function WelcomeScreen({ user, onLogout }) {
  return (
    <div className="dashboard-shell">
      <section className="dashboard-hero">
        <div className="dashboard-hero-content">
          <div className="dashboard-hero-badge">✓ Login Successful</div>
          <h1>Welcome, {user?.name || "User"}! 🎉</h1>
          <p>
            You are now signed in to the JMS workspace. From here, you can
            manage your recruitment, training, and growth workflows with ease.
          </p>
        </div>
      </section>

      <section className="dashboard-panel">
        <div className="dashboard-card">
          <div className="dashboard-brand">
            <img src={Logo} alt="JMS logo" className="brand-logo" />
          </div>

          <h2>Account Overview</h2>

          <div className="user-details-grid">
            <div className="user-detail-card">
              <span>Email Address</span>
              <strong>{user?.email || "Not available"}</strong>
            </div>

            <div className="user-detail-card">
              <span>Username</span>
              <strong>{user?.name || "Not available"}</strong>
            </div>
          </div>

          <button type="button" className="secondary-button" onClick={onLogout}>
            Back to Login
          </button>
        </div>
      </section>
    </div>
  );
}

export default WelcomeScreen;
