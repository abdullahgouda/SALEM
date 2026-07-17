import { useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import langIcon from "../../assets/icons/Language-icon.png";
import logoutIcon from "../../assets/icons/LogOut-icon.png";

function Header({ onLogout, onMenuClick }) {
    const location = useLocation();
    const { i18n, t } = useTranslation();

    const pageTitles = {
        "/dashboard": t("home"),
        "/dashboard/reports": t("reports"),
        "/dashboard/workflow": t("workflow"),
        "/dashboard/streets-history": t("streets"),
        "/dashboard/statistics": t("statistics"),
        "/dashboard/notifications": t("notifications"),
        "/dashboard/users": t("users"),
        "/dashboard/settings": t("settings"),
    };

    const title = pageTitles[location.pathname] || t("dashboard");

    const changeLanguage = () => {
        const newLang = i18n.language === "ar" ? "en" : "ar";
        i18n.changeLanguage(newLang);
        document.documentElement.dir =
            newLang === "ar" ? "rtl" : "ltr";
        document.documentElement.lang = newLang;
        localStorage.setItem("lang", newLang);
    };

    return (
        <header
            dir={i18n.language === "ar" ? "rtl" : "ltr"}
            className="h-14 sm:h-16 bg-white border-b flex items-center justify-between px-4 sm:px-6 gap-2"
        >
            {/* زرار الموبايل */}
            <button
                onClick={onMenuClick}
                className="lg:hidden text-2xl"
            >
                ☰
            </button>

            <h2 className="font-extrabold text-gray-800 text-sm sm:text-base truncate flex-1 min-w-0 mx-2">
                {title}
            </h2>

            <div className="flex items-center gap-2 sm:gap-6 text-xs sm:text-sm flex-shrink-0">
                <button
                    onClick={changeLanguage}
                    className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition"
                >
                    <img src={langIcon} alt="language" className="w-4 h-4" />
                    {i18n.language === "ar" ? "EN" : "عربي"}
                </button>

                <button
                    onClick={onLogout}
                    className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-red-500 font-semibold hover:text-red-600 transition"
                >
                    <img src={logoutIcon} alt="logout" className="w-4 h-4" />
                    {t("logout")}
                </button>
            </div>
        </header>
    );
}

export default Header;
