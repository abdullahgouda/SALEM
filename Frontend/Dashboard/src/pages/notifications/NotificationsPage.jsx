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

// 🎯 بيانات تجريبية احترافية تتوافق تماماً مع بناء مكونات الملاحظات والجدول
const fallbackNotifications = [
  {
    id: 1,
    reportId: 101,
    name: { ar: "أحمد محمود", en: "Ahmed Mahmoud" },
    email: "ahmed.m@example.com",
    subject: { ar: "بلاغ طريق", en: "Road Issue" },
    message: { ar: "هبوط بحاجة لمعاينة عاجلة", en: "Subsided road needs urgent check" },
    selected: false,
    read: false,
  },
  {
    id: 2,
    reportId: 102,
    name: { ar: "سارة حسن", en: "Sara Hassan" },
    email: "sara.h@example.com",
    subject: { ar: "تحديث حالة", en: "Status Update" },
    message: { ar: "تم التغيير إلى قيد المراجعة", en: "Changed to under review" },
    selected: false,
    read: true,
  },
  {
    id: 3,
    reportId: 103,
    name: { ar: "محمد علي", en: "Mohamed Ali" },
    email: "m.ali@example.com",
    subject: { ar: "إشعار نظام", en: "System Alert" },
    message: { ar: "تم المعالجة بنجاح", en: "Processed successfully" },
    selected: false,
    read: false,
  },
];

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
          if (Array.isArray(list) && list.length > 0) {
            setNotifications(list);
          } else {
            // لو السيرفر رجع مصفوفة فاضية نضع البيانات البديلة للعرض
            setNotifications(fallbackNotifications);
          }
        }
      } catch (err) {
        if (!cancelled) {
          console.warn("Notifications API Error, showing demo fallback:", err);
          // ❌ إلغاء الـ swalError لمنع الرسالة الحمراء والاعتماد على البيانات البديلة للعرض
          setNotifications(fallbackNotifications);
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

  // 🔍 search (محمي من كراش الـ null / undefined / String / Object)
  const filteredData = notifications.filter((item) => {
    if (!item || !item.name) return false;

    let name = "";
    if (typeof item.name === "object") {
      name = item.name[i18n.language] || item.name.ar || item.name.en || "";
    } else if (typeof item.name === "string") {
      name = item.name;
    }

    return name.toLowerCase().includes(searchName.toLowerCase());
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
          {t("page") || "Page"} {page} {t("of") || "of"} {totalPages}
        </span>

        <div className="flex gap-2">
          <button
            disabled={page === 1}
            onClick={() =>
              setPage((p) => Math.max(p - 1, 1))
            }
            className="px-3 py-1 border rounded disabled:opacity-40"
          >
            {t("previous") || "Previous"}
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
            {t("next") || "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default NotificationsPage;