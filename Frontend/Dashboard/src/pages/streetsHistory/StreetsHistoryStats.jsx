import { useTranslation } from "react-i18next";
import clockIcon from "../../assets/icons/clock.png";
import mostFreqIcon from "../../assets/icons/most-freq.png";
import totalRepIcon from "../../assets/icons/total-rep.png";

function formatDuration(duration) {
    if (!duration) return "-";

    // duration جاي string زي: "4:50:00"
    const parts = duration.split(":");
    if (parts.length < 2) return duration;

    const hours = parseInt(parts[0], 10);
    const minutes = parseInt(parts[1], 10);

    return `${hours} ${hours === 1 ? "hour" : "hours"} ${minutes} ${minutes === 1 ? "minute" : "minutes"}`;
}

function StreetsHistoryStats({ stats }) {
    const { t } = useTranslation();

    const total = stats?.total_incidents ?? 0;
    const mostCommon = stats?.most_common_priority ?? "-";
    const avgTime = formatDuration(stats?.average_resolution_time);

    const cards = [
        {
            title: t("avgStatusTime"),
            value: avgTime,
            icon: clockIcon,
        },
        {
            title: t("mostFrequentProblem"),
            value: mostCommon,
            icon: mostFreqIcon,
        },
        {
            title: t("totalReportsCount"),
            value: total,
            icon: totalRepIcon,
        },
    ];

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {cards.map((item, index) => (
                <div
                    key={index}
                    className="bg-gradient-to-t from-[#00816F] to-[#2DDBC9]
                    rounded-xl px-6 py-4 text-white flex flex-col gap-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">
                            {item.title}
                        </span>
                        <img
                            src={item.icon}
                            alt={item.title}
                            className="w-7 h-7 opacity-90"
                        />
                    </div>

                    <div className="h-px bg-white/40" />

                    <div className="flex flex-col items-center text-center gap-4">
                        <span className="text-lg font-extrabold">
                            {item.value}
                        </span>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default StreetsHistoryStats;
