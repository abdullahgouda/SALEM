import client from "./axios_client";

// ✅ GET notifications
export const getNotifications = async () => {
  const res = await client.get("/notifications/");

  return res.data.map((n) => ({
    id: n.id,

    name: {
      en: n.name || "",
      ar: n.name || "",
    },

    email: n.email || "",

    subject: {
      en: n.subject || "",
      ar: n.subject || "",
    },

    message: {
      en: n.message || "",
      ar: n.message || "",
    },

    priority: (n.priority || "low").toLowerCase(),

    reportId: n.report_id,

    selected: false,

    read: n.read || false,

    createdAt: n.created_at || null,
  }));
};

// ✅ mark as read
export const markNotificationRead = async (id) => {
  const res = await client.patch(
    `/notifications/${id}/read/`
  );

  return res.data;
};