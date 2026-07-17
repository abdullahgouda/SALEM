import { useState } from "react";
import { useTranslation } from "react-i18next";

import searchIcon from "../../assets/icons/search-icon.png";

function UsersFilters({
    onSearchChange,
    onRoleChange,
    onAddUser,
}) {
    const [search, setSearch] = useState("");
    const [focused, setFocused] = useState(false);

    const { t } = useTranslation();

    return (
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center gap-3 mb-5 -mt-4">

            {/* Search */}
            <div
                className={`
                    flex items-center gap-2
                    bg-white px-3 py-2
                    rounded-full
                    shadow-[0_2px_4px_rgba(0,0,0,0.12)]
                    w-full lg:flex-1
                    ${focused ? "ring-2 ring-[#2DDBC9]" : ""}
                `}
            >
                <img
                    src={searchIcon}
                    alt="search"
                    className="w-4 h-4"
                />

                <input
                    type="text"
                    value={search}
                    onFocus={() => setFocused(true)}
                    onBlur={() => setFocused(false)}
                    onChange={(e) => {
                        setSearch(e.target.value);
                        onSearchChange(e.target.value);
                    }}
                    placeholder={t("searchUsers")}
                    className="w-full text-sm outline-none bg-transparent"
                />
            </div>

            {/* Role Filter */}
            <select
    onChange={(e) => onRoleChange(e.target.value)}
    className="
        h-10 w-full lg:w-44
        px-3 text-sm
        border border-gray-200
        rounded-full
        shadow-[0_2px_4px_rgba(0,0,0,0.12)]
        focus:outline-none focus:ring-2 focus:ring-[#2DDBC9]
    "
>
    <option value="admin">
    {t("admin")}
</option>

<option value="operator">
    {t("employee")}
</option>

<option value="technical">
    {t("fieldWorker")}
</option>

<option value="supervisior">
    {t("distributionOfficer")}
</option>
</select>

            {/* Add User */}
            <button
                onClick={onAddUser}
                className="
                    h-10 px-4 rounded-xl
                    flex items-center justify-center gap-2
                    text-sm font-semibold
                    text-white
                    bg-gradient-to-t from-[#00816F] to-[#2DDBC9]
                    whitespace-nowrap
                "
            >
                {t("addNewUser")}
            </button>
        </div>
    );
}

export default UsersFilters;