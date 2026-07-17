import { useTranslation } from "react-i18next";
import eyeIcon from "../../assets/icons/eyes.png";

const statusMap = {
  New: "new",

  Assigned: "assigned",

  In_Progress: "inProgress",

  Review: "inReview",

  Forworded: "forwarded",

  Finished: "solved",
};

function ReportsTableRows({ reports = [], onView }) {
  const { t, i18n } = useTranslation();

  const isArabic = i18n.language === "ar";

  const statusColor = (status) => {
    switch (status) {
      case "solved":
        return "text-green-600";

      case "new":
        return "text-orange-500";

      case "assigned":
        return "text-blue-600";

      case "inProgress":
        return "text-purple-600";

      case "inReview":
        return "text-yellow-600";

      case "forwarded":
        return "text-cyan-600";

      case "rejected":
        return "text-red-500";

      default:
        return "text-gray-500";
    }
  };

  const priorityColor = (priority) => {
    switch (priority) {
      case "high":
        return "text-red-600";

      case "medium":
        return "text-yellow-500";

      case "low":
        return "text-green-600";

      default:
        return "text-gray-500";
    }
  };

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="bg-white rounded-xl shadow mt-2 divide-y overflow-x-auto"
    >
      {reports.map((report, index) => {
        const rawStatus =
          typeof report.status === "object"
            ? report.status?.name
            : report.status;

        const normalizedStatus =
          statusMap[rawStatus] || "new";

        return (
          <div
            key={`${report.id}-${index}`}
            className="grid grid-cols-8 items-center text-center px-4 py-3 text-sm gap-2"
          >
            {/* ID */}
            <div className="font-bold text-primary truncate">
              {report.id}
            </div>

            {/* Category */}
            <div className="truncate">
              {t(report.category?.toLowerCase().replace(/\s/g, ""))}
            </div>

            {/* Location */}
            <div className="truncate">
              {report.location}
            </div>

            {/* Date */}
            <div className="truncate">
              {report.date}
            </div>

            {/* Status */}
            <div
              className={`font-semibold truncate ${statusColor(
                normalizedStatus
              )}`}
            >
              {t(normalizedStatus)}
            </div>

            {/* Entity */}
            <div className="truncate">
              {t(report.entity?.toLowerCase().replace(/\s/g, ""))}
            </div>

            {/* Priority */}
            <div
              className={`font-semibold truncate ${priorityColor(
                report.priority
              )}`}
            >
              {t(report.priority)}
            </div>

            {/* View */}
            <div className="flex justify-center">
              <button
                onClick={() => onView(report)}
                className="hover:scale-110 transition"
              >
                <img
                  src={eyeIcon}
                  alt="view"
                  className="w-4 h-4 sm:w-5 sm:h-5"
                />
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default ReportsTableRows;