import { useTranslation } from "react-i18next";

function WorkflowHeader({ reports }) {
    const { t, i18n } = useTranslation();

    const items = [
        { key: "new", color: "red" },
        { key: "assigned", color: "blue" },
        { key: "inProgress", color: "yellow" },
        { key: "review", color: "purple" },
        { key: "forwarded", color: "indigo" },
        { key: "done", color: "green" },
    ];

    const colorMap = {
        red: "bg-red-500",
        blue: "bg-blue-500",
        yellow: "bg-yellow-400",
        purple: "bg-purple-500",
        indigo: "bg-indigo-500",
        green: "bg-green-500",
    };

    return (
        <div
            dir={i18n.language === "ar" ? "rtl" : "ltr"}
            className="bg-gradient-to-r from-[#00816F] to-[#2DDBC9] rounded-xl text-white px-2 sm:px-4 md:px-6 py-3">
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 sm:gap-4">
                {items.map((item) => {
                    const count = reports.filter(
                        (r) => r.status === item.key
                    ).length;

                    return (
                        <div
                            key={item.key}
                            className="flex items-center justify-center gap-1 sm:gap-2 text-[10px] sm:text-xs md:text-sm font-semibold whitespace-nowrap">
                            <span
                                className={`w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full ${colorMap[item.color]}`}
                            />

                            <span className="truncate max-w-[90px] sm:max-w-none">
                                {t(item.key)}
                            </span>

                            <span>({count})</span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

export default WorkflowHeader;
