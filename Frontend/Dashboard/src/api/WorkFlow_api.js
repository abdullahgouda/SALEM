import client from "./axios_client";

// ================= STATUS MAP =================
const mapStatus = (status) => {
  switch (status) {
    case "New":
      return "new";

    case "Assigned":
      return "assigned";

    case "In_Progress":
      return "inProgress";

    case "Review":
      return "review";

    case "Forworded":
      return "forwarded";

    case "Completed":
      return "done";

    default:
      return "new";
  }
};

// ================= FORMAT REPORT =================
const formatReports = (incidences = []) => {
  return incidences.map((r) => ({
    id: r.id,

    title: r.Department?.name || "Report",

    location: r.Location_Name || "Unknown",

    time: r.Created_At?.split("T")[0] || "",

    unit: "day",

    status: mapStatus(r.Status),

    priority: r.Priority || "low",
  }));
};

// ================= GET WORKFLOW REPORTS =================
export const getWorkflowReports = async () => {
  const [
    newRes,
    assignedRes,
    progressRes,
    reviewRes,
    forwardedRes,
    completedRes,
  ] = await Promise.all([
    client.get("/incidence/new/"),

    client.get("/incidence/assigned/"),

    client.get("/incidence/in-progress/"),

    client.get("/incidence/review/"),

    client.get("/incidence/forworded/"),

    client.get("/incidence/completed/"),
  ]);

  return [
    ...formatReports(newRes.data?.incidences),

    ...formatReports(assignedRes.data?.incidences),

    ...formatReports(progressRes.data?.incidences),

    ...formatReports(reviewRes.data?.incidences),

    ...formatReports(forwardedRes.data?.incidences),

    ...formatReports(completedRes.data?.incidences),
  ];
};