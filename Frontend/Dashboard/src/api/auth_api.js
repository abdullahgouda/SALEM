// api/auth_api.js
import client from "./axios_client";

// ✅ LOGIN
export const login = async (national_id, password) => {
  const res = await client.post("/employee/login/", {
    national_id,
    password,
  });

  const data = res.data;

  // 🔥 حل المشكلة هنا
  localStorage.setItem("access", data.Asscess_Token);
  localStorage.setItem("refresh", data.Refresh_Token);

  // optional
  localStorage.setItem(
    "user",
    JSON.stringify({
      name: data.Name,
      role: data.Role,
      type: data.User_type,
    })
  );

  return data;
};
// ✅ SIGNUP
export const signup = async (userData) => {
  const res = await client.post("/employee/signup/", userData);
  return res.data;
};

// ✅ FORGOT PASSWORD
export const forgotPassword = async (email) => {
  const res = await client.post("/password/forgot/", { email });
  return res.data;
};

// ✅ VERIFY OTP
export const verifyOtp = async (email, otp) => {
  const res = await client.post("/password/verify-otp/", {
    email,
    otp,
  });

  return res.data;
};

// ✅ RESET PASSWORD
export const resetPassword = async (email, otp, new_password) => {
  const res = await client.post("/password/reset/", {
    email,
    otp,
    new_password,
  });

  return res.data;
};

// ✅ LOGOUT
export const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("user");
};