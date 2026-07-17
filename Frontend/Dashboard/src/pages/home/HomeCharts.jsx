import { useTranslation } from "react-i18next";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

function ChartsHome({ lineData = [], donutData = [] }) {

  const { t, i18n } = useTranslation();

  const isArabic = i18n.language === "ar";

  const COLORS = {
    road: "#6377F1",
    electricity: "#69C78C",
    gas: "#F4A949",
    other: "#8B5CF6",
    "no department": "#2DDBC9",
  };

  const getTranslatedName = (name) => {

    const lower = name?.toLowerCase();

    if (lower === "no department") {
      return t("noDepartment");
    }

    return t(lower);
  };

  const total = donutData.reduce(
    (sum, item) => sum + item.value,
    0
  );

  const renderCustomLabel = ({
    cx,
    cy,
    midAngle,
    outerRadius,
    name,
    value,
    fill,
  }) => {

    const RADIAN = Math.PI / 180;

    const radius = outerRadius + 5;

    const x1 =
      cx +
      outerRadius *
      Math.cos(-midAngle * RADIAN);

    const y1 =
      cy +
      outerRadius *
      Math.sin(-midAngle * RADIAN);

    const x2 =
      cx +
      radius *
      Math.cos(-midAngle * RADIAN);

    const y2 =
      cy +
      radius *
      Math.sin(-midAngle * RADIAN);

    const x3 =
      x2 + (x2 > cx ? 20 : -20);

    const y3 = y2;

    return (
      <g>

        <path
          d={`M${x1},${y1} L${x2},${y2} L${x3},${y3}`}
          stroke={fill}
          fill="none"
        />

        <text
          x={x3}
          y={y3 - 4}
          textAnchor={
            x3 > cx ? "start" : "end"
          }
          className="text-xs fill-gray-700"
        >
          {getTranslatedName(name)}
        </text>

        <text
          x={x3}
          y={y3 + 10}
          textAnchor={
            x3 > cx ? "start" : "end"
          }
          className="text-xs font-bold"
          fill={fill}
        >
          {value}
        </text>
      </g>
    );
  };

  return (

    <div
      dir={isArabic ? "ltr" : "rtl"}
      className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-4 sm:gap-6 w-full min-w-0"
    >

      {/* ================= LINE CHART ================= */}
      <div className="bg-white rounded-xl sm:rounded-2xl p-3 shadow-sm min-w-0 overflow-hidden">

        <div className="flex items-center justify-between mb-3">

          <h3 className="font-bold text-sm text-gray-800">
            {t("monthlyReports")}
          </h3>

        </div>

        <div className="w-full h-[200px] sm:h-[220px] min-h-[180px]">

          <ResponsiveContainer width="100%" height="100%">

            <LineChart data={lineData}>

              <XAxis
                dataKey="day"
                axisLine={false}
                tickLine={false}
                tick={{
                  fontSize: 10,
                  fill: "#9CA3AF",
                }}
              />

              <YAxis
                axisLine={false}
                tickLine={false}
                tick={{
                  fontSize: 12,
                  fill: "#9CA3AF",
                }}
                allowDecimals={false}
              />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="value"
                stroke="#00816F"
                strokeWidth={2}
                dot={{ r: 2 }}
                activeDot={{ r: 4 }}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>
      </div>

      {/* ================= DONUT CHART ================= */}
      <div className="bg-white rounded-xl sm:rounded-2xl p-3 sm:p-4 shadow-sm flex flex-col items-center">

        <div className="w-full max-w-[300px] h-[220px]">

          <ResponsiveContainer width="100%" height="100%">

            <PieChart>

              <Pie
                data={donutData}
                dataKey="value"
                cx="50%"
                cy="50%"
                innerRadius={40}
                outerRadius={90}
                labelLine={false}
                label={renderCustomLabel}
              >

                {donutData.map((item, i) => (

                  <Cell
                    key={i}
                    fill={
                      COLORS[
                      item.name.toLowerCase()
                      ] || "#2DDBC9"
                    }
                  />

                ))}

              </Pie>

              <text
                x="50%"
                y="50%"
                textAnchor="middle"
                dominantBaseline="middle"
                className="text-2xl font-extrabold fill-gray-800"
              >
                {total}
              </text>

            </PieChart>

          </ResponsiveContainer>

        </div>

        <div className="flex flex-wrap justify-center gap-3 mt-2 text-xs">

          {donutData.map((item, i) => (

            <div
              key={i}
              className="flex items-center gap-1 text-gray-600"
            >

              <span
                className="w-2.5 h-2.5 rounded-full"
                style={{
                  backgroundColor:
                    COLORS[
                    item.name.toLowerCase()
                    ] || "#2DDBC9",
                }}
              />

              <span>
                {getTranslatedName(item.name)}
              </span>

            </div>

          ))}

        </div>
      </div>
    </div>
  );
}

export default ChartsHome;