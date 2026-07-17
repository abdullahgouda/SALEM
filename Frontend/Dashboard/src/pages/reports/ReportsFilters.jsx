import { useState } from "react";
import { useTranslation } from "react-i18next";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

import searchIcon from "../../assets/icons/search-icon.png";
import filterIcon from "../../assets/icons/filter-icon.png";
import calendarIcon from "../../assets/icons/calendar.png";

function ReportsFilters({
  departments = [],
  statuses = [],
  onDepartmentChange,
  onStatusChange,
  onDateChange,
  onSearchChange,
}) {
  const { t, i18n } = useTranslation();

  const isArabic = i18n.language === "ar";

  const [showFilters, setShowFilters] = useState(false);

  const [date, setDate] = useState(null);

  const statusTranslations = {
    New: t("new"),

    Assigned: t("assigned"),

    In_Progress: t("inProgress"),

    Review: t("inReview"),

    Forworded: t("forwarded"),

    Finished: t("solved"),
  };

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="flex items-center gap-2 relative -mt-5"
    >
      {/* Search */}
      <div className="relative">
        <input
          type="text"
          placeholder={t("searchById")}
          onChange={(e) => onSearchChange(e.target.value)}
          className={`h-8 w-52 text-sm border border-gray-200 rounded-full
          shadow-[0_2px_4px_rgba(0,0,0,0.12)]
          focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]
          ${
            isArabic
              ? "pr-10 text-right"
              : "pl-10 text-left"
          }`}
        />

        <img
          src={searchIcon}
          alt="search"
          className={`absolute top-1/2 -translate-y-1/2 w-4 h-4
          ${isArabic ? "right-3" : "left-3"}`}
        />
      </div>

      {/* Filter Button */}
      <button
        onClick={() => setShowFilters(!showFilters)}
        className="h-8 w-8 flex items-center justify-center rounded-full
        bg-[#2DDBC9] shadow-[0_2px_4px_rgba(0,0,0,0.12)]"
      >
        <img
          src={filterIcon}
          alt="filter"
          className="w-4 h-4"
        />
      </button>

      {/* Filters */}
      {showFilters && (
        <div className="flex items-center gap-2">
          {/* Date */}
          <div className="relative">
            <DatePicker
              selected={date}
              onChange={(newDate) => {
                setDate(newDate);
                onDateChange(newDate);
              }}
              placeholderText={t("dateFilter")}
              className={`h-8 w-40 text-sm border border-gray-200 rounded-full
              shadow-[0_2px_4px_rgba(0,0,0,0.12)]
              focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]
              cursor-pointer
              ${
                isArabic
                  ? "pr-8 text-right"
                  : "pl-8 text-left"
              }`}
            />

            <img
              src={calendarIcon}
              alt="calendar"
              className={`absolute top-1/2 -translate-y-1/2 w-4 h-4
              ${isArabic ? "right-3" : "left-3"}`}
            />
          </div>

          {/* Department */}
          <select
            onChange={(e) =>
              onDepartmentChange(e.target.value)
            }
            className="h-8 w-40 px-3 text-sm border border-gray-200 rounded-full
            shadow-[0_2px_4px_rgba(0,0,0,0.12)]
            focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]"
          >
            <option value="">
              {t("entityFilter")}
            </option>

            {departments.map((dept) => (
              <option
                key={dept.id}
                value={dept.id}
              >
                {t(dept.name.toLowerCase())}
              </option>
            ))}
          </select>

          {/* Status */}
          <select
            onChange={(e) =>
              onStatusChange(e.target.value)
            }
            className="h-8 w-40 px-3 text-sm border border-gray-200 rounded-full
            shadow-[0_2px_4px_rgba(0,0,0,0.12)]
            focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]"
          >
            <option value="">
              {t("statusFilter")}
            </option>

            {statuses.map((st) => (
              <option
                key={st.id}
                value={st.id}
              >
                {statusTranslations[st.name] || st.name}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
}

export default ReportsFilters;