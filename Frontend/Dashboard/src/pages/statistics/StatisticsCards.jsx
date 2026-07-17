import { useState, useEffect } from "react";

import { useTranslation } from "react-i18next";

import { getStatisticsCards } from "../../api/statistics_api";

function StatisticsCards({ filters }) {
  const { t, i18n } =
    useTranslation();

  const isArabic =
    i18n.language === "ar";

  const [data, setData] =
    useState({
      solvedToday: 0,
      transferred: 0,
      inReview: 0,
      open: 0,
      total: 0,
    });

  useEffect(() => {
    getStatisticsCards(filters)
      .then(setData)
      .catch((err) =>
        console.error(
          "Statistics Cards Error:",
          err
        )
      );
  }, [filters]);

  const cards = [
    {
      title: t("solvedToday"),
      value: data.solvedToday,
    },

    {
      title: t("transferred"),
      value: data.transferred,
    },

    {
      title: t("inReview"),
      value: data.inReview,
    },

    {
      title: t("openReports"),
      value: data.open,
    },

    {
      title: t("totalReports"),
      value: data.total,
    },
  ];

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 mb-6"
    >
      {cards.map((card, i) => (
        <div
          key={i}
          className="bg-white rounded-lg px-3 py-2 flex justify-between items-center shadow"
        >
          <div>
            <p className="text-[11px] text-gray-500">
              {card.title}
            </p>

            <p className="text-lg font-extrabold text-[#00816F]">
              {card.value.toLocaleString()}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default StatisticsCards;