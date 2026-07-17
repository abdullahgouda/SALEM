import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useState } from "react";
import { useTranslation } from "react-i18next";

// ❌ القديم
// import { validatePasswordResetToken } from "../../services/authService";

// ✅ الجديد
import { verifyOtp } from "../../api/auth_api";

import { error as swalError } from "../../utils/swal";

function Verification() {
    const navigate = useNavigate();
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    const [code, setCode] = useState("");

    return (
        <motion.div
            dir={isArabic ? "rtl" : "ltr"}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
            className="text-center">

            {/* Title */}
            <h2 className="text-base md:text-lg font-extrabold mb-2">
                {t("verificationTitle")}
            </h2>

            {/* Description */}
            <p className="text-xs md:text-sm text-gray-500 mb-6">
                {t("verificationDesc")}
            </p>

            <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder={t("enterCode")}
                className="w-full px-4 py-2 mb-2 border rounded-xl text-lg
                transition-colors duration-200 hover:border-[#2DDBC9] focus:outline-none focus:ring-2
                focus:ring-[#2DDBC9]"
            />

            {/* Button */}
            <motion.button
                whileHover={{ scale: 1.015 }}
                whileTap={{ scale: 0.98 }}
                transition={{ duration: 0.12 }}
                onClick={async () => {
                    if (!code) {
                        swalError(t("verificationTitle"), t("enterCode"));
                        return;
                    }

                    const email = localStorage.getItem("reset_email");

                    if (!email) {
                        swalError(t("verificationTitle"), "Missing email");
                        return;
                    }

                    try {
                        // ✅ الجديد
                        await verifyOtp(email, code);

                        localStorage.setItem("reset_token", code);

                        navigate("/set-new-password");

                    } catch (err) {
                        const msg =
                            err.response?.data?.detail ||
                            err.response?.data?.errors ||
                            err.response?.data?.message ||
                            t("enterCode");

                        swalError(
                            t("verificationTitle"),
                            typeof msg === "string" ? msg : JSON.stringify(msg)
                        );
                    }
                }}
                className="w-full py-2.5 rounded-xl text-white font-semibold
                bg-gradient-to-r from-[#00816F] to-[#2DDBC9]">
                {t("verify")}
            </motion.button>

            {/* Back */}
            <div className="mt-6 flex justify-between text-xs">
                <Link
                    to="/login"
                    className="text-[#00816F] font-semibold hover:text-[#2DDBC9]">
                    {t("loginButton")}
                </Link>
            </div>
        </motion.div>
    );
}

export default Verification;