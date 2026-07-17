import client from "./axios_client";

const COLORS = [
  "#00816F",
  "#2DDBC9",
  "#7C3AED",
  "#F97316",
  "#22C55E",
  "#EF4444",
];

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
    console.error("Home API Error:", error);

    return {
      cards: {
        total: 0,
        open: 0,
        inReview: 0,
        transferred: 0,
        solvedToday: 0,
      },

      lineChart: [],

      donutChart: [],

      reports: [],
    };
  }
};