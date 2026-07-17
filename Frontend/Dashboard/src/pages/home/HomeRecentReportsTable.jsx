import { useTranslation } from "react-i18next";

function HomeRecentReportsTable({ reports = [] }) {
  const { t, i18n } = useTranslation();

  const isArabic = i18n.language === "ar";

  const statusMap = {
    New: {
      key: "new",
      style: "bg-orange-100 text-orange-700",
    },

    Assigned: {
      key: "assigned",
      style: "bg-blue-100 text-blue-700",
    },

    In_Progress: {
      key: "inProgress",
      style: "bg-purple-100 text-purple-700",
    },

    Review: {
      key: "inReview",
      style: "bg-yellow-100 text-yellow-700",
    },

    Forworded: {
      key: "forwarded",
      style: "bg-cyan-100 text-cyan-700",
    },

    Finished: {
      key: "solved",
      style: "bg-green-100 text-green-700",
    },
  };

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="bg-white rounded-xl shadow-sm overflow-x-auto text-center"
    >
      <table className="w-full text-xs sm:text-sm min-w-[400px]">
        <thead className="bg-gradient-to-r from-[#00816F] to-[#2DDBC9] text-white">
          <tr>
            <th className="px-2 sm:px-4 py-2 font-bold">
              {t("reportId")}
            </th>

            <th className="px-2 sm:px-4 py-2">
              {t("date")}
            </th>

            <th className="px-2 sm:px-4 py-2">
              {t("status")}
            </th>

            <th className="px-2 sm:px-4 py-2">
              {t("entity")}
            </th>
          </tr>
        </thead>

        <tbody>
          {reports.map((r) => (
            <tr
              key={r.Incidence_Number}
              className="border-b last:border-0 hover:bg-gray-50 transition"
            >
              <td className="px-2 sm:px-4 py-2 font-bold text-black">
                {r.Incidence_Number}
              </td>

              <td className="px-2 sm:px-4 py-2 whitespace-nowrap">
                {r.Date ? String(r.Date).split("T")[0] : ""}
              </td>

              <td className="px-2 sm:px-4 py-2">
                <span
                  className={`px-2 rounded-full text-xs font-semibold ${
                    statusMap[r.Status]?.style ||
                    "bg-gray-100 text-gray-700"
                  }`}
                >
                  {t(statusMap[r.Status]?.key || r.Status)}
                </span>
              </td>

              <td className="px-2 sm:px-4 py-2">
                {t(r.Department?.name?.toLowerCase())}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HomeRecentReportsTable;