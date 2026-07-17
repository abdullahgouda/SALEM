import { useTranslation } from "react-i18next";

function NotificationsTableHeader() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className=" mt-4  bg-gradient-to-r from-[#00816F] to-[#2DDBC9] text-white 
            rounded-xl  px-2 sm:px-4 py-2 sm:py-3  font-semibold  text-[10px] sm:text-xs md:text-sm">
            <div className="grid grid-cols-5 text-center gap-1 sm:gap-2">
                <div className={isArabic ? "text-right pr-6" : "text-left pl-6"}>
                    {t("name")}
                </div>

                <div>{t("email")}</div>

                <div>{t("subject")}</div>

                <div>{t("message")}</div>

                <div>{t("actions")}</div>
            </div>
        </div>
    );
}

export default NotificationsTableHeader;
