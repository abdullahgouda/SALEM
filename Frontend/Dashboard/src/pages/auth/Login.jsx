import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { motion } from "framer-motion";
import { Eye, EyeOff } from "lucide-react";
import { useTranslation } from "react-i18next";

function Login() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    const [nationalId, setNationalId] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();

        // 1. تخزين توكن وهمي عشان الـ DashboardLayout يسمح بالدخول
        localStorage.setItem("token", "dummy_token_123");
        localStorage.setItem("access_token", "dummy_token_123");
        localStorage.setItem("user", JSON.stringify({ name: "Admin" }));

        // 2. التوجيه المباشر للدشبورد
        navigate("/dashboard", { replace: true });
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
                    className="w-full py-2.5 rounded-xl text-white font-semibold 
                    bg-gradient-to-r from-[#00816F] to-[#2DDBC9]"
                >
                    {t("loginButton")}
                </button>
            </form>
        </motion.div>
    );
}

export default Login;