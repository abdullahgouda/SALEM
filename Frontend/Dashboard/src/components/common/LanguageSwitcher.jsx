import { useTranslation } from "react-i18next";
import langIcon from "../../assets/icons/Language-icon.png";

function LanguageSwitcher() {
    const { i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    const changeLanguage = () => {
        const newLang = isArabic ? "en" : "ar";
        i18n.changeLanguage(newLang);

        document.documentElement.dir =
            newLang === "ar" ? "rtl" : "ltr";

        document.documentElement.lang = newLang;
        localStorage.setItem("lang", newLang);
    };

    return (
        <button
            onClick={changeLanguage}
            className={` absolute top-6 z-50 ${isArabic ? "left-6" : "right-6"}
            flex items-center gap-1.5 px-2 py-1 text-xs rounded-md
            bg-gray-100 hover:bg-gray-200 transition`}>
            <img
                src={langIcon}
                alt="language"
                className="w-3.5 h-3.5"
            />
            {isArabic ? "EN" : "عربي"}
        </button>
    );
}

export default LanguageSwitcher;
