import { useTranslation } from "react-i18next";
import noStreetsHis from "../../assets/noreviews.png";

function StreetsHistoryEmpty() {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className={`flex flex-col items-center justify-center h-full text-center gap-7 ${isArabic ? "text-right" : "text-left"}`}>
            <img
                src={noStreetsHis}
                alt="No Reports"
                className="w-80 opacity-90"/>
            <h3 className="text-lg font-bold text-gray-700">
                {t("streetsHistoryEmpty")}
            </h3>
        </div>
    );
}

export default StreetsHistoryEmpty;
