import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useState } from "react";
import { useTranslation } from "react-i18next";



// ✅ الجديد
import { resetPassword } from "../../api/auth_api";

import { success as swalSuccess, error as swalError } from "../../utils/swal";

function SetNewPassword() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";
    const navigate = useNavigate();
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);

    return (
        <motion.div
            dir={isArabic ? "rtl" : "ltr"}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}>

            <h2 className="text-base md:text-lg font-extrabold mb-4 text-center">
                {t("setNewPassword")}
            </h2>

            <div className="space-y-4">

                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder={t("setNewPassword")}
                    className="w-full px-4 py-2.5 border rounded-xl text-sm
                    transition-colors duration-200
                    hover:border-[#2DDBC9] focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]"
                />

                <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder={t("confirmPassword")}
                    className="w-full px-4 py-2.5 border rounded-xl text-sm
                    transition-colors duration-200
                    hover:border-[#2DDBC9] focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]"
                />

            </div>

            <motion.button
                whileHover={{ scale: 1.015 }}
                whileTap={{ scale: 0.98 }}
                transition={{ duration: 0.12 }}
                onClick={async () => {
                    const token = localStorage.getItem("reset_token");
                    const email = localStorage.getItem("reset_email");

                    if (!token || !email) {
                        swalError(t("setNewPassword"), "Missing reset data");
                        return;
                    }

                    if (!password || password !== confirmPassword) {
                        swalError(t("setNewPassword"), t("confirmPassword"));
                        return;
                    }

                    setLoading(true);

                    try {
                        // ✅ الجديد
                        await resetPassword(email, token, password);

                        localStorage.removeItem("reset_token");
                        localStorage.removeItem("reset_email");

                        await swalSuccess(t("setNewPassword"), t("loginButton"));

                        navigate("/login");

                    } catch (err) {
                        const msg =
                            err.response?.data?.detail ||
                            err.response?.data?.message ||
                            "Reset failed";

                        swalError(
                            t("setNewPassword"),
                            typeof msg === "string" ? msg : JSON.stringify(msg)
                        );
                    } finally {
                        setLoading(false);
                    }
                }}
                className="w-full mt-6 py-2.5 rounded-xl text-white font-semibold
                bg-gradient-to-r from-[#00816F] to-[#2DDBC9]">
                {loading ? (t("loading") || "Loading...") : t("createNewPassword")}
            </motion.button>

        </motion.div>
    );
}

export default SetNewPassword;