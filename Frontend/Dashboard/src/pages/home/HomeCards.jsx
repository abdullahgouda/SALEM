import { useTranslation } from "react-i18next";

import solvedIcon from "../../assets/icons/solved.png";
import transferredIcon from "../../assets/icons/transferred.png";
import reviewIcon from "../../assets/icons/review.png";
import openIcon from "../../assets/icons/open.png";
import totalIcon from "../../assets/icons/total.png";

function HomeCards({ data }) {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    if (!data) return null;

    const cards = [
        { title: t("solvedToday"), value: data.solvedToday, icon: solvedIcon },
        { title: t("transferred"), value: data.transferred, icon: transferredIcon },
        { title: t("inReview"), value: data.inReview, icon: reviewIcon },
        { title: t("openReports"), value: data.open, icon: openIcon },
        { title: t("totalReports"), value: data.total, icon: totalIcon },
    ];

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-2 sm:gap-3">
            {cards.map((card, index) => (
                <div
                    key={index}
                    className={`bg-white rounded-lg px-2 sm:px-3 py-2 flex items-center shadow-[0_2px_4px_rgba(0,0,0,0.12)]
                    ${isArabic ? "justify-between text-right" : "justify-between text-left"}`}>
                    {/* Text */}
                    <div className="min-w-0 flex-1">
                        <p className="text-[10px] sm:text-[11px] text-gray-500 truncate">
                            {card.title}
                        </p>
                        <p className="text-base sm:text-lg font-extrabold text-[#00816F] truncate">
                            {card.value}
                        </p>
                    </div>

                    {/* Icon */}
                    <img src={card.icon} alt="" className="w-6 h-6 sm:w-8 sm:h-8 flex-shrink-0" />
                </div>
            ))}
        </div>
    );
}

export default HomeCards;
