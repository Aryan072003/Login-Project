import { useState } from "react";
import Logo from "../assets/jms-logo.webp";

function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setIsSubmitting(true);
    setMessage("");

    try {
      const response = await fetch("/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        setMessage(data.message || "Login failed. Please try again.");
        return;
      }

      setEmail("");
      setPassword("");
      setMessage("");
      onLoginSuccess?.(data.user);
    } catch {
      setMessage("Unable to reach the server. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-welcome-section">
       <div className="login-welcome-section-content">
          <div className="welcome-badge">✳</div>

          <div className="welcome-copy">
            <h1 className="welcome-header">Hello JMS! 👋</h1>
            <p className="welcome-text">
              Helping businesses and MSMEs hire, train, and grow efficiently
              through technology.
            </p>
          </div>

          <p className="welcome-footer">
            &copy; 2026 JMS. All rights reserved.
          </p>
        </div>
        </div>

        <p className="welcome-footer">&copy; 2026 JMS. All rights reserved.</p>
      </div>

      <div className="login-card">
        <div className="login-brand">
          <img src={Logo} alt="JMS logo" className="brand-logo" />
          <span className="brand-name">JMS</span>
        </div>

        <div className="login-header">
          <h2>Welcome Back!</h2>
          <p>
            Sign in to continue managing your hiring, training, and growth
            workflows.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <label className="field-group">
            <input
              type="email"
              placeholder="Enter Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <label className="field-group">
            <input
              type="password"
              placeholder="Enter Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Signing In..." : "Login Now"}
          </button>
        </form>

        {message ? (
          <p className="message" aria-live="polite">
            {message}
          </p>
        ) : null}
      </div>
    </div>
  );
}

export default Login;

