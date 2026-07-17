import client from "./axios_client";

// ================= GET STREETS HISTORY =================
export const getStreetsHistory = async (params = {}) => {
  const queryParams = {};

  // ===== Search By Street =====
  if (params.street) {
    queryParams.location_name = params.street;
  }

  // ===== Date =====
  if (params.date) {
    queryParams.date = params.date;
  }

  // ===== Priority =====
  if (params.priority) {
    queryParams.priority = params.priority;
  }

  // ===== API REQUEST =====
  const res = await client.get(
    "/home/incidence/location-analysis/",
    {
      params: queryParams,
    }
  );

  const data = res.data || {};

  const incidences = data.incidences || [];

  // ================= FORMAT RECORDS =================
  const records = incidences.map((r) => ({
    id: r.Incidence_Number,

    date: r.Date
      ? r.Date.split("T")[0]
      : "",

    category:
      r.Department?.name || "Other",

    status:
      r.Status === "Completed"
        ? "solved"
        : r.Status === "Assigned"
        ? "inProgress"
        : "underReview",

    repairTime:
      r.Solve_Duration || "-",

    process:
      r.Department?.name || "Other",

    location:
      data.Location_Name || "Cairo",

    latitude:
      r.Lat,

    longitude:
      r.Long,
  }));

  // ================= RETURN =================
  return {
    records,

    stats: {
      total_incidents:
        data.Total_Incidences_On_Street || 0,

      most_common_priority:
        data.Most_Frequent_Department?.name || "-",

      average_resolution_time:
        data.Average_Solve_Duration || "-",
    },

    count: records.length,
  };
};