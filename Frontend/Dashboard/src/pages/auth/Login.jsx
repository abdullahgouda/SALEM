import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { motion } from "framer-motion";
import { Eye, EyeOff } from "lucide-react";
import { useTranslation } from "react-i18next";
import { error as swalError } from "../../utils/swal";

// ✅ API
import { login } from "../../api/auth_api";

function Login() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    const [nationalId, setNationalId] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        // ✅ Validation
        if (!nationalId || !password) {
            return swalError("Error", "Please fill all fields");
        }

        setLoading(true);

        try {
            await login(nationalId, password);

            // ✅ Redirect بعد النجاح
            navigate("/dashboard", { replace: true });

        } catch (err) {
            const msg =
                err.response?.data?.detail ||
                err.response?.data?.message ||
                "Login failed";

            swalError("Login Error", msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div
            dir={isArabic ? "rtl" : "ltr"}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
        >
            {/* Title */}
            <h2 className="text-base md:text-lg font-extrabold mb-2">
                {t("loginTitle")}
            </h2>

            {/* Description */}
            <p className="text-xs md:text-sm text-gray-500 mb-6">
                {t("loginDesc")}
            </p>

            <form className="space-y-4" onSubmit={handleLogin}>

                {/* National ID */}
                <div>
                    <label className="block text-sm mb-1">
                        {t("nationalId")}
                    </label>
                    <input
                        type="text"
                        maxLength="14"
                        inputMode="numeric"
                        value={nationalId}
                        placeholder={t("enterNationalId")}
                        className="w-full px-3 py-2 border rounded-md text-sm"
                        onChange={(e) => setNationalId(e.target.value)}
                    />
                </div>

                {/* Password */}
                <div>
                    <label className="block text-sm mb-1">
                        {t("password")}
                    </label>

                    <div className="relative">
                        <input
                            type={showPassword ? "text" : "password"}
                            value={password}
                            placeholder={t("enterPassword")}
                            className="w-full px-3 py-2 border rounded-md text-sm"
                            onChange={(e) => setPassword(e.target.value)}
                        />

                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className={`absolute top-2 ${isArabic ? "left-3" : "right-3"}`}
                        >
                            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>
                    </div>
                </div>

                {/* Forgot Password */}
                <div className={isArabic ? "text-right" : "text-left"}>
                    <Link
                        to="/forget-password"
                        className="text-xs text-[#00816F]"
                    >
                        {t("forgotPassword")}
                    </Link>
                </div>

                {/* Submit */}
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-2.5 rounded-xl text-white font-semibold 
                    bg-gradient-to-r from-[#00816F] to-[#2DDBC9] 
                    disabled:opacity-70"
                >
                    {loading ? (t("loading") || "Loading...") : t("loginButton")}
                </button>
            </form>
        </motion.div>
    );
}

export default Login;