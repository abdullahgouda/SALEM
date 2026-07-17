import React from "react";
import { motion } from "framer-motion";
import { assets } from "../assets/assets";
import { useTranslation } from "react-i18next";

// Animations
const fadeUp = {
    hidden: { opacity: 0, y: 50 },
    show: { opacity: 1, y: 0, transition: { duration: 0.8 } }
};

const fadeRight = {
    hidden: { opacity: 0, x: -50 },
    show: { opacity: 1, x: 0, transition: { duration: 0.8 } }
};

const stagger = {
    hidden: {},
    show: { transition: { staggerChildren: 0.15 } }
};

const DownloadApp = () => {
    const { t } = useTranslation();

    return (
        <section id="DownloadApp"
            className="w-full bg-[#0C111D] pt-20 sm:pt-10 lg:pt-10 pb-10">
            <motion.div
                variants={stagger}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true }}
                className="max-w-7xl mx-auto px-6 lg:px-20 w-full flex flex-col lg:flex-row items-center justify-between gap-12 text-white">

                {/* TEXT */}
                <div className="w-full lg:w-1/2 flex flex-col gap-5">
                    <motion.p
                        variants={fadeRight}
                        className="text-[#1B4374] uppercase font-semibold tracking-wide text-sm">
                        {t("download_small")}
                    </motion.p>

                    <motion.h2
                        variants={fadeRight}
                        className="text-2xl sm:text-3xl lg:text-4xl font-bold leading-snug">
                        {t("download_title")}
                    </motion.h2>

                    <motion.p
                        variants={fadeRight}
                        className="text-gray-300 text-sm sm:text-base leading-relaxed">
                        {t("download_desc1")}
                    </motion.p>

                    <motion.p
                        variants={fadeRight}
                        className="text-gray-400 text-sm">
                        {t("download_desc2")}
                    </motion.p>

                    <motion.p
                        variants={fadeRight}
                        className="text-[#C45038] font-bold text-lg sm:text-xl">
                        {t("download_now")}
                    </motion.p>

                    {/* STORE BUTTONS */}
                    <motion.div
                        variants={fadeRight}
                        className="flex gap-4 mt-4">
                        <a href="#" className="transition-transform hover:scale-105">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg"
                                alt="Google Play" className="h-12 sm:h-14"/>
                        </a>

                        <a href="#" className="transition-transform hover:scale-105">
                            <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg"
                                alt="App Store" className="h-12 sm:h-14"/>
                        </a>
                    </motion.div>
                </div>

                {/* IMAGE */}
                <motion.div
                    variants={fadeUp}
                    className="w-full lg:w-1/2 flex justify-center">
                    <motion.img src={assets.mobile}
                        alt="phone preview" className="w-[280px] sm:w-[320px] lg:w-[380px]"
                    />
                </motion.div>
            </motion.div>
        </section>
    );
};

export default DownloadApp;
