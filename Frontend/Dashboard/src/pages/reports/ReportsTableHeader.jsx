import { useTranslation } from "react-i18next";

function ReportsTableHeader() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className="mt-4 bg-gradient-to-r from-[#00816F] to-[#2DDBC9]
            text-white rounded-xl px-2 sm:px-4 py-2 sm:py-3 font-semibold
            text-[10px] sm:text-xs md:text-sm">

            <div className=" grid grid-cols-8 text-center gap-1 sm:gap-2">
                <div className="truncate font-bold">
                    {t("reportId")}
                </div>

                <div className="truncate">
                    {t("category")}
                </div>

                <div className="truncate">
                    {t("location")}
                </div>

                <div className="truncate">
                    {t("date")}
                </div>

                <div className="truncate">
                    {t("status")}
                </div>

                <div className="truncate">
                    {t("entity")}
                </div>

                <div className="truncate">
                    {t("priority")}
                </div>

                <div className="truncate">
                    {t("actions")}
                </div>
            </div>
        </div>
    );
}

export default ReportsTableHeader;
