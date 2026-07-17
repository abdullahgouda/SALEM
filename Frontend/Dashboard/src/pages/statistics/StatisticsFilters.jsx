import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function StatisticsFilters({ onChange }) {
  const { t, i18n } = useTranslation();

  const isArabic = i18n.language === "ar";

  const today = new Date()
    .toISOString()
    .split("T")[0];

  const [startDate, setStartDate] =
    useState("2026-05-01");

  const [endDate, setEndDate] =
    useState("2026-05-10");

  useEffect(() => {
    onChange?.({
      startDate,
      endDate,
    });
  }, [startDate, endDate]);

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="bg-white rounded-xl shadow-sm p-1 mb-2  overflow-hidden">
        
      <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-end justify-between">
        
        {/* ===== TITLE ===== */}
        <div>
          <h2 className="text-base sm:text-lg font-bold text-gray-800">            
            {t("statistics")}
          </h2>

          <p className="text-sm text-gray-500 mt-1">
            {t("statisticsDescription")}
          </p>
        </div>

        {/* ===== FILTERS ===== */}
        <div className="flex flex-col sm:flex-row gap-3 w-full lg:w-auto ">
          
          {/* START DATE */}
          <div className="h-7 flex flex-col gap-1">
            <label className="text-xs text-gray-500 font-medium">
              {t("fromDate")}
            </label>

            <input
              lang="en"
              type="date"
              value={startDate}
              max={today}
              onChange={(e) =>
                setStartDate(e.target.value)
              }
              className="h-7 px-4 rounded-xl border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]"
            />
          </div>

          {/* END DATE */}
          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500 font-medium">
              {t("toDate")}
            </label>

            <input
              lang="en"
              type="date"
              value={endDate}
              max={today}
              onChange={(e) =>
                setEndDate(e.target.value)
              }
              className="h-6 px-4 rounded-xl border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default StatisticsFilters;