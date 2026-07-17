import { useTranslation } from "react-i18next";
import eyeIcon from "../../assets/icons/eyes.png";

function StreetsHistoryTableRows({ records = [], onView }) {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className="bg-white rounded-xl shadow mt-2 divide-y">
            {records.map((item, index) => (
                <div
                    key={`${item.id}-${index}`}
                    className="grid grid-cols-6 text-sm py-4 px-4 items-center text-center">
                    <div className="font-bold text-[#00816F]">
                        {item.id}
                    </div>

                    <div>{item.date}</div>

                    <div>{t(item.category.toLowerCase())}</div>

                    <div
                        className={`font-semibold ${item.status === "solved"
                                ? "text-green-600"
                                : item.status === "inProgress"
                                ? "text-orange-500" : "text-red-500"}`}>
                        {t(item.status?.toLowerCase())}
                    </div>

                    <div>{t(item.repairTime)}</div>

                    <div className="flex justify-center">
                        <button
                            onClick={() => onView(item)}
                            className="hover:scale-110 transition">
                            <img
                                src={eyeIcon}
                                alt="view"
                                className="w-5 h-5"
                            />
                        </button>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default StreetsHistoryTableRows;
