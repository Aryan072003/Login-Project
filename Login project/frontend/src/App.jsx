import { useState } from "react";
import Login from "./components/Login";
import WelcomeScreen from "./components/WelcomeScreen";
import "./App.css";

function App() {
  const [authenticatedUser, setAuthenticatedUser] = useState(null);
  return authenticatedUser ? (
    <WelcomeScreen
      user={authenticatedUser}
      onLogout={() => setAuthenticatedUser(null)}
    />
  ) : (
    <Login onLoginSuccess={setAuthenticatedUser} />
  );
}

export default App;
