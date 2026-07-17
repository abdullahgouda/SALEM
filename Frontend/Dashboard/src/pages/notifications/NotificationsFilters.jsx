import { useState } from "react";
import { useTranslation } from "react-i18next";

import searchIcon from "../../assets/icons/search-icon.png";
import filterIcon from "../../assets/icons/filter-icon.png";

function NotificationsFilters({ onSearchChange }) {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    const [showFilters, setShowFilters] = useState(false);
    const [type, setType] = useState("");
    const [status, setStatus] = useState("");

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className="flex items-center gap-2 relative -mt-6 -mr-6">
            {/* ===== Search ===== */}
            <div className="relative">
                <input
                    type="text"
                    placeholder={t("searchByName")}
                    onChange={(e) => onSearchChange(e.target.value)}
                    className={`
                        h-7 w-48 text-sm border border-gray-200 rounded-full
                        shadow-[0_2px_4px_rgba(0,0,0,0.12)]
                        focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]
                        ${isArabic ? "pr-10 text-right" : "pl-10 text-left"}
                    `}
                />

                <img
                    src={searchIcon}
                    alt="search"
                    className={` absolute top-1/2 -translate-y-1/2 w-4 h-4  ${isArabic ? "right-3" : "left-3"}`}
                />
            </div>

            {/* ===== Filter Button ===== */}
            <button
                type="button"
                onClick={() => setShowFilters((prev) => !prev)}
                className="h-7 w-7 flex items-center justify-center
                rounded-full bg-[#2DDBC9] shadow-[0_2px_4px_rgba(0,0,0,0.12)]">
                <img src={filterIcon} alt="filter" className="w-4 h-4" />
            </button>

            {/* ===== Filters Dropdown ===== */}
            {showFilters && (
                <div className="flex items-center gap-2">

                    {/* Type */}
                    <select
                        value={type}
                        onChange={(e) => setType(e.target.value)}
                        className="h-7 w-40 px-3 text-sm border border-gray-200 rounded-full
                        shadow-[0_2px_4px_rgba(0,0,0,0.12)] focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]">
                        <option value="">{t("type")}</option>
                        <option value="urgent">{t("urgent")}</option>
                        <option value="normal">{t("normal")}</option>
                    </select>

                    {/* Status */}
                    <select
                        value={status}
                        onChange={(e) => setStatus(e.target.value)}
                        className="h-7 w-32 px-3 text-sm border border-gray-200 rounded-full
                        shadow-[0_2px_4px_rgba(0,0,0,0.12)] focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]">
                        <option value="">{t("status")}</option>
                        <option value="read">{t("read")}</option>
                        <option value="unread">{t("unread")}</option>
                    </select>

                </div>
            )}
        </div>
    );
}

export default NotificationsFilters;
