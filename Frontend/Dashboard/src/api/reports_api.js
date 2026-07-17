import client from "./axios_client";

// ================= GET REPORTS =================
export const getReports = async (params = {}) => {
  const queryParams = {};

  if (params.search) {
    queryParams.Search = params.search;
  }

  if (params.department) {
    queryParams.Department = params.department;
  }

  if (params.status) {
    queryParams.Status = params.status;
  }

  if (params.dateFrom) {
    queryParams.Date = params.dateFrom;
  }

  const res = await client.get("/incidence/", {
    params: queryParams,
  });

  const incidences = res.data?.incidences || [];

  return incidences.map((r) => ({
    id: r.id,

    category: r.Department?.name || "Other",

    location: r.Location_Name || "Unknown",

    date: r.Created_At?.split("T")[0],

    status: r.Status || "New",

    entity: r.Department?.name || "Other",

    priority: r.Priority || "low",

    beforeImage: r.Image_Before_Analysis,

    afterImage: r.Image_After_Analysis,

    aiAnalysis: r.Ai_Analysis_Label_Before,

    latitude: r.Latlatitude,

    longitude: r.Longitude,

    description: r.Description,
  }));
};

// ================= GET SINGLE REPORT =================
export const getReportById = async (id) => {
  const res = await client.get("/incidence/");

  const incidences = res.data?.incidences || [];

  const r = incidences.find((item) => item.id === id);

  if (!r) return null;

  return {
    id: r.id,

    category: r.Department?.name || "Other",

    location: r.Location_Name || "Unknown",

    date: r.Created_At?.split("T")[0],

    status: r.Status || "New",

    entity: r.Department?.name || "Other",

    priority: r.Priority || "low",

    beforeImage: r.Image_Before_Analysis,

    afterImage: r.Image_After_Analysis,

    aiAnalysis: r.Ai_Analysis_Label_Before,

    latitude: r.Latlatitude,

    longitude: r.Longitude,

    description: r.Description,
  };
};

// ================= GET DEPARTMENTS =================
export const getDepartments = async () => {
  return [
    { id: "Electricity", name: "Electricity" },

    { id: "Gas", name: "Gas" },

    { id: "Other", name: "Other" },
  ];
};

// ================= GET STATUSES =================
export const getIncidentStatuses = async () => {
  return [
    { id: "New", name: "New" },

    { id: "Assigned", name: "Assigned" },

    { id: "In_Progress", name: "In_Progress" },

    { id: "Review", name: "Review" },

    { id: "Forworded", name: "Forworded" },

    { id: "Finished", name: "Finished" },
  ];
};