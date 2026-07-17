import { useEffect, useState } from "react";

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

import {
  MapContainer,
  TileLayer,
  useMap,
} from "react-leaflet";

import L from "leaflet";

import "leaflet/dist/leaflet.css";
import "leaflet.heat";

import {
  getLineChartData,
  getDonutData,
  getHeatPoints,
} from "../../api/statistics_api";

function HeatLayer({ points }) {
  const map = useMap();

  useEffect(() => {
    if (!map || !points.length)
      return;

    const heatLayer = L.heatLayer(
      points,
      {
        radius: 25,
        blur: 15,
        maxZoom: 12,
      }
    );

    heatLayer.addTo(map);

    return () => {
      map.removeLayer(heatLayer);
    };
  }, [map, points]);

  return null;
}

function StatisticsChart({ filters }) {

  const { t, i18n } = useTranslation();

  const isArabic =
    i18n.language === "ar";

  const [lineData, setLineData] =
    useState([]);

  const [donutData, setDonutData] =
    useState([]);

  const [heatPoints, setHeatPoints] =
    useState([]);

  useEffect(() => {
    const loadCharts =
      async () => {
        try {
          const [
            line,
            donut,
            heat,
          ] = await Promise.all([
            getLineChartData(filters),

            getDonutData(filters),

            getHeatPoints(),
          ]);

          setLineData(line || []);

          setDonutData(donut || []);

          setHeatPoints(heat || []);
        } catch (error) {
          console.error(
            "Statistics Charts Error:",
            error
          );
        }
      };

    loadCharts();
  }, [filters]);

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

    const x3 = x2 + (x2 > cx ? 80 : -80);

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

  const total = donutData.reduce(
    (s, i) => s + i.value,
    0
  );

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="space-y-2"
    >
      {/* ===== LINE CHART ===== */}
      <div className="bg-white rounded-2xl p-4 shadow-sm">
        <ResponsiveContainer
          width="100%"
          height={200}
        >
          <LineChart data={lineData}>
            <XAxis dataKey="day" />

            <YAxis
              allowDecimals={false}
              tickMargin={15}
            />
            
            <Tooltip />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#00816F"
              strokeWidth={3}
              dot={{ r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* ===== DONUT + MAP ===== */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* ===== MAP ===== */}
        <div className="bg-white rounded-2xl p-3 shadow-sm h-[300px] overflow-hidden">
          <MapContainer
            center={[30.0444, 31.2357]}
            zoom={11}
            style={{
              height: "100%",
              width: "100%",
            }}
          >
            <TileLayer url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png" />

            <HeatLayer
              points={heatPoints}
            />
          </MapContainer>
        </div>

        {/* ===== DONUT ===== */}
        <div className="bg-white rounded-2xl p-2 shadow-sm flex flex-col items-center justify-center">
          <ResponsiveContainer
            width="100%"
            height={220}
          >
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
                      ]
                    }
                  />
                ))}
              </Pie>

              <text
                x="50%"
                y="50%"
                textAnchor="middle"
                dominantBaseline="middle"
                className="text-2xl font-extrabold fill-[#00816F]"
              >
                {total}
              </text>
            </PieChart>
          </ResponsiveContainer>

          <div className="flex flex-wrap justify-center gap-3 mt-2 text-xs">
            {donutData.map(
              (item, i) => (
                <div
                  key={i}
                  className="flex items-center gap-1 text-gray-600"                >
                  <span
                    className="w-3 h-3 rounded-full"
                    style={{
                      backgroundColor:
                        COLORS[item.name.toLowerCase()],
                    }}
                  />

                  <span>
                    {getTranslatedName(item.name)}</span>
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default StatisticsChart;