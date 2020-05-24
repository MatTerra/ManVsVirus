import React, { createContext, useState, useEffect, useMemo } from "react";
import jwtDecode from "jwt-decode";

export const AuthContext = createContext();

const Auth = ({ children }) => {
  const [currentUser, setCurrentUser] = useState({});
  const [token, setToken] = useState("");

  useEffect(() => {
    setToken(localStorage.getItem("loginToken"));
  }, []);

  useEffect(() => {
    try {
      let decode = jwtDecode(token);
      setCurrentUser({
        email: decode.email,
        role: decode.role,
        isLoggedIn: true,
      });
    } catch (error) {
      setCurrentUser({});
    }
  }, [token]);

  const handleUser = useMemo(
    () => ({
      data: currentUser,
      logout: () => setCurrentUser({}),
    }),
    [currentUser]
  );

  return (
    <AuthContext.Provider value={handleUser}>{children}</AuthContext.Provider>
  );
};

export default Auth;