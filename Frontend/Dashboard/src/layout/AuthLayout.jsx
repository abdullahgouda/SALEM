import { Outlet } from "react-router-dom";
import logo from "../assets/logow.png";
import pattern from "../assets/pattern.png";
import { useTranslation } from "react-i18next";
import LanguageSwitcher from "../components/common/LanguageSwitcher";

function AuthLayout() {
    const { i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className="relative min-h-screen grid grid-cols-1 lg:grid-cols-2"
        >
            {/* زرار اللغة فوق */}
            <LanguageSwitcher />

            {/* Right Side - Branding */}
            <div className="relative hidden lg:flex items-center justify-center overflow-hidden bg-gradient-to-r from-[#00816F] to-[#2DDBC9]">

                <img
                    src={pattern}
                    alt="Pattern Background"
                    className="absolute inset-0 w-full h-full object-cover opacity-30"
                />

                <img
                    src={logo}
                    alt="Salem Logo"
                    className="relative z-10 w-64 object-contain"
                />
            </div>

            {/* Left Side - Form */}
            <div className="flex items-center justify-center px-6 bg-white">
                <div className="w-full max-w-md">
                    <Outlet />
                </div>
            </div>
        </div>
    );
}

export default AuthLayout;
