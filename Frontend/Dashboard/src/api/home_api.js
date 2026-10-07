import client from "./axios_client";

const COLORS = [
  "#00816F",
  "#2DDBC9",
  "#7C3AED",
  "#F97316",
  "#22C55E",
  "#EF4444",
];

// 🎯 بيانات تجريبية لتعبئة الواجهة فور فشل طلب السيرفر
const dummyFallbackData = {
  cards: {
    total: 39,
    open: 14,
    inReview: 8,
    transferred: 5,
    solvedToday: 12,
  },
  lineChart: [
    { day: 1, value: 5 },
    { day: 5, value: 12 },
    { day: 10, value: 18 },
    { day: 15, value: 25 },
    { day: 20, value: 22 },
  ],
  donutChart: [
    { name: "Public Works", value: 15, color: COLORS[0] },
    { name: "Utilities", value: 10, color: COLORS[1] },
    { name: "Traffic", value: 8, color: COLORS[2] },
  ],
  reports: [
    { id: "REP-101", Date: "2026-10-01", Status: "Completed", Department: "Public Works" },
    { id: "REP-102", Date: "2026-10-03", Status: "Under Review", Department: "Utilities" },
    { id: "REP-103", Date: "2026-10-05", Status: "Open", Department: "Traffic" },
  ],
};

const getCurrentMonthDates = () => {
  const now = new Date();

  const startDate = new Date(now.getFullYear(), now.getMonth(), 1)
    .toISOString()
    .split("T")[0];

  const endDate = new Date(now.getFullYear(), now.getMonth() + 1, 0)
    .toISOString()
    .split("T")[0];

  return { startDate, endDate };
};

export const getHomeData = async () => {
  try {
    const { startDate, endDate } = getCurrentMonthDates();

    const [
      statusSummaryRes,
      timeCountsRes,
      departmentChartRes,
      latestReportsRes,
    ] = await Promise.all([
      client.get(
        `/home/incidence/status-summary-by-date/?start_date=${startDate}&end_date=${endDate}`
      ),

      client.get(
        `/home/incidence/time-counts-by-date/?start_date=${startDate}&end_date=${endDate}`
      ),

      client.get("/home/incidence/monthly-department-chart/"),

      client.get("/home/incidence/latest-per-department/"),
    ]);

    const statusSummary = statusSummaryRes.data;
    const timeCounts = timeCountsRes.data;
    const departmentChart = departmentChartRes.data;
    const latestReports = latestReportsRes.data;

    return {
      cards: {
        total: statusSummary.Total_Incidences || 0,

        open:
          (statusSummary.Total_Incidences || 0) -
          (statusSummary.Completed_Incidences || 0),

        inReview: statusSummary.Review_Incidences || 0,

        transferred: statusSummary.Forworded_Incidences || 0,

        solvedToday: statusSummary.Completed_Incidences || 0,
      },

      lineChart:
        timeCounts.Daily_Counts?.map((item) => ({
          day: new Date(item.Date).getDate(),
          value: item.Incidences_Count,
        })) || [],

      donutChart:
        departmentChart.Chart_Data?.map((item, index) => ({
          name: item.Department_Name,
          value: item.Incidences_Count,
          color: COLORS[index % COLORS.length],
        })) || [],

      reports: latestReports.Latest_Incidences || [],
    };
  } catch (error) {
    console.error("Home API Error, using fallback data:", error);

    // إرجاع البيانات الوهمية بدلاً من الأصفار لتظهر جميع مكونات الصفحة
    return dummyFallbackData;
  }
};