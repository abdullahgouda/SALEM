import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useState } from "react";
import { useTranslation } from "react-i18next";


// ✅ الجديد
import { forgotPassword } from "../../api/auth_api";

import { success as swalSuccess, error as swalError } from "../../utils/swal";

function ForgetPassword() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);

    return (
        <motion.div
            dir={isArabic ? "rtl" : "ltr"}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }} >

            <h2 className="text-base md:text-lg font-extrabold mb-2">
                {t("forgetPassword")}
            </h2>

            <p className="text-xs md:text-sm text-gray-500 mb-6 ">
                {t("forgetPasswordDesc")}
            </p>

            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder={t("email")}
                className="w-full px-4 py-2.5 border rounded-xl text-sm mb-4
                transition-colors duration-200
                hover:border-[#2DDBC9] focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]" />

            <motion.button
                whileHover={{ scale: 1.015 }}
                whileTap={{ scale: 0.98 }}
                transition={{ duration: 0.12 }}
                onClick={async () => {
                    if (!email) return;

                    setLoading(true);
                    try {
                        // ✅ الجديد
                        await forgotPassword(email);

                        localStorage.setItem("reset_email", email);

                        await swalSuccess(t("sendCode"), t("verificationDesc"));

                        navigate("/verification");
                    } catch (err) {
                        const msg =
                            err.response?.data?.detail ||
                            err.response?.data?.message ||
                            "Request failed";

                        swalError(
                            t("forgetPassword"),
                            typeof msg === "string" ? msg : JSON.stringify(msg)
                        );
                    } finally {
                        setLoading(false);
                    }
                }}
                className="w-full py-2.5 rounded-xl text-white font-semibold
                bg-gradient-to-r from-[#00816F] to-[#2DDBC9]">
                {loading ? (t("loading") || "Loading...") : t("sendCode")}
            </motion.button>

            <div className="mt-6 flex justify-between text-xs">
                <Link to="/login"
                    className="text-[#00816F] font-semibold hover:text-[#2DDBC9]">
                    {t("loginButton")}
                </Link>
                <Link to="/login"
                    className="text-[#00816F] font-semibold hover:text-[#2DDBC9] text-xs">
                    {t("rememberPassword")}
                </Link>
            </div>

        </motion.div>
    );
}

export default ForgetPassword;