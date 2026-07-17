import client from "./axios_client";

const COLORS = [
  "#00816F",
  "#2DDBC9",
  "#7C3AED",
  "#F97316",
  "#22C55E",
  "#EF4444",
];

const getDates = (filters = {}) => {
  return {
    startDate:
      filters?.startDate ||
      "2026-05-01",

    endDate:
      filters?.endDate ||
      "2026-05-31",
  };
};

// ================= CARDS =================
export const getStatisticsCards =
  async (filters = {}) => {
    const { startDate, endDate } =
      getDates(filters);

    const res = await client.get(
      "/home/incidence/status-summary-by-date/",
      {
        params: {
          start_date: startDate,
          end_date: endDate,
        },
      }
    );

    const d = res.data || {};

    return {
      solvedToday:
        d.Completed_Incidences || 0,

      transferred:
        d.Forworded_Incidences || 0,

      inReview:
        d.Review_Incidences || 0,

      open:
        d.Assigned_And_In_Progress_Incidences ||
        0,

      total:
        d.Total_Incidences || 0,
    };
  };

// ================= LINE CHART =================
export const getLineChartData =
  async (filters = {}) => {
    const { startDate, endDate } =
      getDates(filters);

    const res = await client.get(
      "/home/incidence/time-counts-by-date/",
      {
        params: {
          start_date: startDate,
          end_date: endDate,
        },
      }
    );

    return (
      res.data?.Daily_Counts?.map(
        (item) => ({
          day: new Date(
            item.Date
          ).getDate(),

          value:
            item.Incidences_Count,
        })
      ) || []
    );
  };

// ================= DONUT =================
export const getDonutData =
  async (filters = {}) => {
    const { startDate, endDate } =
      getDates(filters);

    const res = await client.get(
      "/home/incidence/department-summary-by-date/",
      {
        params: {
          start_date: startDate,
          end_date: endDate,
        },
      }
    );

    return (
      res.data?.Departments?.map(
        (item, index) => ({
          name:
            item.Department_Name,

          value:
            item.Incidences_Count,

          color:
            COLORS[
              index %
                COLORS.length
            ],
        })
      ) || []
    );
  };

// ================= HEATMAP =================
export const getHeatPoints =
  async () => {
    const res = await client.get(
      "/home/incidence/heatmap/"
    );

    return (
      res.data?.Heatmap_Data?.map(
        (item) => [
          item.Latlatitude,
          item.Longitude,
          item.Incidences_Count,
        ]
      ) || []
    );
  };