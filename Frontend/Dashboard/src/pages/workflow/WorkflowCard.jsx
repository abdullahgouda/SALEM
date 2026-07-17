import { useTranslation } from "react-i18next";

function WorkflowCard({ report }) {
  const { t, i18n } = useTranslation();

  const priorityColors = {
    high: "bg-red-500",
    medium: "bg-yellow-400",
    low: "bg-green-500",
  };

  return (
    <div
      dir={i18n.language === "ar" ? "rtl" : "ltr"}
      className="relative bg-white rounded-xl shadow-sm p-3 sm:p-4">
      <div
            className={`absolute ${ i18n.language === "ar"
            ? "right-0 rounded-tr-xl rounded-br-xl" : "left-0 rounded-tl-xl rounded-bl-xl"
            } top-0 h-full w-2 sm:w-3 ${
                priorityColors[report.priority]
            }`}
        />


      <div className="flex flex-col gap-1 text-[11px] sm:text-xs md:text-sm">
        <span className="font-bold text-gray-800 truncate">
          {t(report.title.toLowerCase())}
        </span>

        <span className="text-gray-500 truncate">
          {report.location}
        </span>

        <span className="text-gray-400 text-[10px] sm:text-xs">
          {report.time} {t(report.unit)}
        </span>
      </div>
    </div>
  );
}

export default WorkflowCard;
