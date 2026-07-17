import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { getHomeData } from "../../api/home_api";

import HomeCards from "./HomeCards";
import HomeCharts from "./HomeCharts";
import HomeRecentReportsTable from "./HomeRecentReportsTable";

function HomePage() {
  const { i18n } = useTranslation();

  const [data, setData] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        const res = await getHomeData();

        setData(res);
      } catch (err) {
        console.error("Error loading home data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="w-full flex items-center justify-center py-20 text-gray-500">
        Loading...
      </div>
    );
  }

  if (!data) return null;

  return (
    <div
      key={i18n.language}
      className="flex flex-col gap-3 sm:gap-4 pb-6 sm:pb-8 w-full max-w-full overflow-x-hidden"
    >
      <HomeCards data={data.cards} />

      <HomeCharts
        lineData={data.lineChart}
        donutData={data.donutChart}
      />

      <HomeRecentReportsTable reports={data.reports} />
    </div>
  );
}

export default HomePage;