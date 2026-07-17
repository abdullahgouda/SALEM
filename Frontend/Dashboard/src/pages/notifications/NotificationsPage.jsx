import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

import NotificationsFilters from "./NotificationsFilters";
import NotificationsTableHeader from "./NotificationsTableHeader";
import NotificationsTableRows from "./NotificationsTableRows";
import EmptyNotifications from "./EmptyNotifications";

import {
  getNotifications,
  markNotificationRead,
} from "../../api/notifications_api";

import { error as swalError } from "../../utils/swal";

function NotificationsPage() {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const isArabic = i18n.language === "ar";

  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [searchName, setSearchName] = useState("");

  const rowsPerPage = 12;

  useEffect(() => {
    let cancelled = false;

    const fetchNotifications = async () => {
      try {
        setLoading(true);

        const list = await getNotifications();

        if (!cancelled) {
          setNotifications(Array.isArray(list) ? list : []);
        }
      } catch (err) {
        if (!cancelled) {
          setNotifications([]);

          const msg =
            err.response?.data?.detail ||
            err.response?.data?.message ||
            "Error loading notifications";

          swalError(t("notifications") || "Notifications", msg);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    fetchNotifications();

    const interval = setInterval(() => {
      fetchNotifications();
    }, 10000);

    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  // 🔍 search
  const filteredData = notifications.filter((item) => {
    const name = item.name[i18n.language] || "";

    return name
      .toLowerCase()
      .includes(searchName.toLowerCase());
  });

  const totalPages = Math.max(
    1,
    Math.ceil(filteredData.length / rowsPerPage) || 1
  );

  useEffect(() => {
    setPage((p) => Math.min(p, totalPages));
  }, [totalPages]);

  const startIndex = (page - 1) * rowsPerPage;

  const visibleData = filteredData.slice(
    startIndex,
    startIndex + rowsPerPage
  );

  const isNextDisabled =
    startIndex + rowsPerPage >= filteredData.length ||
    page >= totalPages;

  // ✅ select
  const handleSelect = (id) => {
    setNotifications((prev) =>
      prev.map((item) =>
        item.id === id
          ? {
              ...item,
              selected: !item.selected,
            }
          : item
      )
    );
  };

  // ✅ delete (frontend only)
  const handleDelete = (id) => {
    setNotifications((prev) =>
      prev.filter((item) => item.id !== id)
    );
  };

  // ✅ go to report + mark as read
  const handleGo = async (reportId) => {
    const row = notifications.find(
      (n) => n.reportId === reportId
    );

    const notifyId = row?.id;

    if (notifyId != null) {
      try {
        await markNotificationRead(notifyId);

        setNotifications((prev) =>
          prev.map((n) =>
            n.id === notifyId
              ? { ...n, read: true }
              : n
          )
        );
      } catch {
        // ignore error
      }
    }

    navigate(`/dashboard/reports/${reportId}`);
  };

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="px-6 py-4 flex flex-col min-h-full"
    >
      <NotificationsFilters
        onSearchChange={(value) => {
          setSearchName(value);
          setPage(1);
        }}
      />

      <NotificationsTableHeader />

      {loading ? (
        <p className="py-8 text-center text-gray-500">
          {t("loading") || "Loading..."}
        </p>
      ) : filteredData.length === 0 ? (
        <EmptyNotifications />
      ) : (
        <NotificationsTableRows
          notifications={visibleData}
          onSelect={handleSelect}
          onDelete={handleDelete}
          onGo={handleGo}
        />
      )}

      {/* ===== Pagination ===== */}
      <div className="mt-auto pt-6 flex items-center justify-between text-sm">
        <span className="text-gray-500">
          {t("page")} {page} {t("of")} {totalPages}
        </span>

        <div className="flex gap-2">
          <button
            disabled={page === 1}
            onClick={() =>
              setPage((p) => Math.max(p - 1, 1))
            }
            className="px-3 py-1 border rounded disabled:opacity-40"
          >
            {t("previous")}
          </button>

          <button
            disabled={isNextDisabled}
            onClick={() =>
              setPage((p) =>
                Math.min(p + 1, totalPages)
              )
            }
            className="px-3 py-1 border rounded disabled:opacity-40"
          >
            {t("next")}
          </button>
        </div>
      </div>
    </div>
  );
}

export default NotificationsPage;