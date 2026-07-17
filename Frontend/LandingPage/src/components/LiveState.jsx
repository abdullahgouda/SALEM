import React from "react";
import { motion } from "framer-motion";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { FaRoad, FaBolt, FaLightbulb, FaWater } from "react-icons/fa";
import { useTranslation } from "react-i18next";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip
);

// ===== Animations =====
const fadeUp = {
    hidden: { opacity: 0, y: 60 },
    show: { opacity: 1, y: 0, transition: { duration: 1 } },
};

const fadeScale = {
    hidden: { opacity: 0, scale: 0.9 },
    show: { opacity: 1, scale: 1, transition: { duration: 0.8 } },
};

const stagger = {
    hidden: {},
    show: { transition: { staggerChildren: 0.15 } },
};

// 🔑 Animation خفيفة للكروت الصغيرة (تحل التعليق)
const cardFade = {
    hidden: { opacity: 0, y: 20 },
    show: {
        opacity: 1,
        y: 0,
        transition: { duration: 0.4, ease: "easeOut" },
    },
};

const LiveState = () => {
    const { t } = useTranslation();

    const smallCards = [
        { label: t("live_small_road"), value: 1240, icon: <FaRoad size={22} /> },
        { label: t("live_small_elec"), value: 620, icon: <FaBolt size={22} /> },
        { label: t("live_small_light"), value: 430, icon: <FaLightbulb size={22} /> },
        { label: t("live_small_water"), value: 390, icon: <FaWater size={22} /> },
    ];

    const data = {
        labels: t("live_days"),
        datasets: [
            {
                data: [40, 48, 60, 62, 55, 22, 20],
                tension: 0.4,
                pointRadius: 4,
                borderWidth: 3,
                borderColor: (ctx) => {
                    const chart = ctx.chart;
                    const { ctx: canvas, chartArea } = chart;
                    if (!chartArea) return "#00BE9B";

                    const gradient = canvas.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                    gradient.addColorStop(0, "#00BE9B");
                    gradient.addColorStop(1, "#1B4374");
                    return gradient;
                },
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            x: { ticks: { color: "white" }, grid: { display: false } },
            y: {
                ticks: { color: "white" },
                grid: { color: "rgba(255,255,255,0.1)" },
            },
        },
    };

    return (
        <section id="LiveState"
            className="relative w-full min-h-screen bg-[#0C111D] text-white px-6 sm:px-10 lg:px-20 py-20">
            {/* TITLE */}
            <motion.div
                variants={fadeUp}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true }}
                className="flex justify-center mb-12">
                <h1 className="bg-white/10 backdrop-blur-lg rounded-3xl px-10 sm:px-20 lg:px-40 py-4 text-xl sm:text-2xl lg:text-4xl font-bold">
                    {t("live_title")}
                </h1>
            </motion.div>

            <div className="grid grid-cols-12 gap-10">

                {/* GRAPH */}
                <motion.div
                    variants={fadeUp}
                    initial="hidden"
                    whileInView="show"
                    viewport={{ once: true }}
                    className="col-span-12 lg:col-span-6 bg-black/30 rounded-2xl p-6 lg:p-10 backdrop-blur-md">
                    <div
                        dir="ltr"
                        className="h-[260px] sm:h-[300px] lg:h-[320px] rounded-2xl bg-gradient-to-b from-[#00BE9B] to-[#1B4374] p-4">
                        <Line data={data} options={options} />
                    </div>
                </motion.div>

                {/* BIG CARDS */}
                <motion.div
                    variants={stagger}
                    initial="hidden"
                    whileInView="show"
                    viewport={{ once: true }}
                    className="col-span-12 lg:col-span-3 flex flex-col gap-10">
                    <motion.div
                        variants={fadeScale}
                        className="rounded-2xl bg-gradient-to-b from-[#00BE9B]/40 to-[#1B4374]/20 backdrop-blur-md p-6 lg:p-8 text-center transition hover:scale-105">
                        <p className="text-3xl sm:text-4xl lg:text-6xl font-bold">2680</p>
                        <p className="opacity-80 mt-2">{t("live_total_incidents")}</p>
                    </motion.div>

                    <motion.div
                        variants={fadeScale}
                        className="rounded-2xl bg-gradient-to-b from-[#00BE9B]/40 to-[#1B4374]/20 backdrop-blur-md p-6 lg:p-8 text-center transition hover:scale-105">
                        <p className="text-2xl sm:text-3xl lg:text-5xl font-bold">3h 25m</p>
                        <p className="opacity-80 mt-2">{t("live_avg_time")}</p>

                        <div className="flex justify-center items-end gap-2 mt-5">
                            {[4, 6, 3, 7, 5, 8, 6].map((h, i) => (
                                <div
                                    key={i}
                                    className="w-2 rounded-full"
                                    style={{
                                        height: h * 7,
                                        background:
                                            "linear-gradient(to top, #00BE9B, #1B4374)",
                                    }}
                                />
                            ))}
                        </div>
                    </motion.div>
                </motion.div>

                {/* SMALL CARDS (FIXED LAG) */}
                <motion.div
                    variants={stagger}
                    initial="hidden"
                    whileInView="show"
                    viewport={{ once: true }}
                    className="col-span-12 lg:col-span-3 grid grid-cols-2 gap-6">
                    {smallCards.map((item, i) => (
                        <motion.div
                            key={i}
                            variants={cardFade}
                            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-xl p-4 flex flex-col justify-between shadow-lg shadow-black/40 transition-transform duration-300 hover:scale-105" >
                            <div className="text-[#00BE9B]">{item.icon}</div>
                            <div>
                                <p className="text-xs sm:text-sm opacity-90">{item.label}</p>
                                <p className="text-lg sm:text-xl font-semibold">
                                    {item.value}
                                </p>
                            </div>
                        </motion.div>
                    ))}
                </motion.div>

            </div>
        </section>
    );
};

export default LiveState;
