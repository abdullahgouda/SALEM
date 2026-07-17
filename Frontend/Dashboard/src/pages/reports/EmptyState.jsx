import { useTranslation } from "react-i18next";
import noReportsImg from "../../assets/noreports.png";

function EmptyState() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className="flex flex-col items-center justify-center h-full text-center gap-7">
            <img
                src={noReportsImg}
                alt="No Reports"
                className="w-80 opacity-90"
            />

            <h3 className="text-lg font-bold text-gray-700">
                {t("noReports")}
            </h3>

            <p className="text-sm text-gray-500 max-w-sm">
                {t("noReportsDesc")}
            </p>
        </div>
    );
}

export default EmptyState;
