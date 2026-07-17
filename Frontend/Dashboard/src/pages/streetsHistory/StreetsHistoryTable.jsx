import { useTranslation } from "react-i18next";

function StreetsHistoryTable() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className="mt-4 bg-gradient-to-r from-[#00816F] to-[#2DDBC9]
            text-white rounded-xl px-4 py-3 text-sm font-semibold">
            <div className="grid grid-cols-6 text-center">
                <div>{t("reportNumberLabel")}</div>
                <div>{t("dateTime")}</div>
                <div>{t("problemType")}</div>
                <div>{t("finalStatus")}</div>
                <div>{t("repairTime")}</div>
                <div>{t("procedures")}</div>
            </div>
        </div>
    );
}

export default StreetsHistoryTable;
