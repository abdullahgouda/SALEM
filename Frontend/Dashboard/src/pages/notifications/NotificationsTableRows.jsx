import { useTranslation } from "react-i18next";

import trashIcon from "../../assets/trash.png";
import arrowIcon from "../../assets/arrow-right.png";

function NotificationsTableRows({
  notifications,
  onSelect,
  onDelete,
  onGo,
}) {
  const { i18n } = useTranslation();

  const isArabic = i18n.language === "ar";

  const priorityColor = {
    high: "bg-red-500",
    medium: "bg-yellow-400",
    low: "bg-green-500",
  };

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="bg-white rounded-xl shadow mt-2 divide-y overflow-x-auto"
    >
      {notifications.map((item) => (
        <div
          key={item.id}
          className={`relative grid grid-cols-5 items-center px-4 py-3 text-sm transition
          ${
            !item.read
              ? "bg-[#EFFFFC] font-semibold"
              : "bg-white"
          }`}
        >
          {/* Priority Bar */}
          <div
            className={`absolute ${
              isArabic ? "right-0" : "left-0"
            } top-0 h-full w-1 ${
              isArabic
                ? "rounded-tr-xl rounded-br-xl"
                : "rounded-tl-xl rounded-bl-xl"
            } ${priorityColor[item.priority]}`}
          />

          {/* Name + Checkbox */}
          <div
            className={`flex items-center gap-2 ${
              isArabic
                ? "text-right pr-3"
                : "text-left pl-3"
            }`}
          >
            <input
              type="checkbox"
              checked={item.selected}
              onChange={() => onSelect(item.id)}
            />

            <span className="truncate">
              {item.name[i18n.language]}
            </span>
          </div>

          {/* Email */}
          <div className="text-center truncate">
            {item.email}
          </div>

          {/* Subject */}
          <div className="text-center truncate">
            {item.subject[i18n.language]}
          </div>

          {/* Message */}
          <div className="text-center text-gray-500 truncate">
            {item.message[i18n.language]}
          </div>

          {/* Actions */}
          <div className="flex justify-center items-center gap-3">
            <button
              onClick={() => onGo(item.reportId)}
            >
              <img
                src={arrowIcon}
                className={`w-4 h-4 ${
                  !isArabic ? "rotate-180" : ""
                }`}
              />
            </button>

            <button
              onClick={() => onDelete(item.id)}
            >
              <img
                src={trashIcon}
                className="w-4 h-4"
              />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default NotificationsTableRows;