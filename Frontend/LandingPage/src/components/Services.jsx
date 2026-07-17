import React from "react";
import { assets } from "../assets/assets";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

// Animation Variants (هادية ومش سريعة)
const fadeUp = {
    hidden: { opacity: 0, y: 40 },
    show: {
        opacity: 1,
        y: 0,
        transition: { duration: 0.9, ease: "easeOut" },
    },
};

const fadeRight = {
    hidden: { opacity: 0, x: 60 },
    show: {
        opacity: 1,
        x: 0,
        transition: { duration: 0.9, ease: "easeOut" },
    },
};

const stagger = {
    hidden: {},
    show: {
        transition: { staggerChildren: 0.2 },
    },
};

const Services = () => {
    const { t } = useTranslation();

    const steps = [
        { num: "01", title: t("step_1_title"), desc: t("step_1_desc") },
        { num: "02", title: t("step_2_title"), desc: t("step_2_desc") },
        { num: "03", title: t("step_3_title"), desc: t("step_3_desc") },
        { num: "04", title: t("step_4_title"), desc: t("step_4_desc") },
    ];

    return (
        <section
            id="Services"
            className="w-full py-14 sm:py-16 lg:py-20 px-6 lg:px-20">
            <div className="max-w-7xl mx-auto flex flex-col lg:flex-row gap-8 items-center">

                {/* IMAGE */}
                <motion.div
                    variants={fadeRight}
                    initial="hidden"
                    whileInView="show"
                    viewport={{ once: true }}
                    className="w-full lg:w-1/2">
                    <img src={assets.road} alt="Service" 
                    className="w-full max-h-[600px] object-cover rounded-3xl shadow-lg"/>
                </motion.div>

                {/* CONTENT */}
                <motion.div
                    variants={stagger}
                    initial="hidden"
                    whileInView="show"
                    viewport={{ once: true }}
                    className="w-full lg:w-1/2 flex flex-col gap-6"
                >
                    {/* Small title */}
                    <motion.p
                        variants={fadeUp}
                        className=" text-[#1B4374] uppercase font-semibold tracking-wide text-xs sm:text-sm lg:text-base ">
                        {t("services_why")}
                    </motion.p>

                    {/* Main title */}
                    <motion.h2
                        variants={fadeUp}
                        className="font-bold leading-snug text-xl sm:text-2xl lg:text-4xl ">
                        <span className="text-[#1B4374]">
                            {t("services_main1")}{" "}
                        </span>
                        <span className="text-[#9A4D3A]">
                            {t("services_main2")}
                        </span>
                    </motion.h2>

                    {/* Steps */}
                    <motion.div
                        variants={stagger}
                        className="flex flex-col gap-8 mt-4"
                    >
                        {steps.map((item, index) => (
                            <motion.div
                                key={index}
                                variants={fadeUp}
                                className="flex flex-col gap-2">
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-[#1B4374] 
                                    flex items-center justify-center text-white font-bold text-sm sm:text-base">
                                        {item.num}
                                    </div>
                                    <h3 className="font-semibold text-sm sm:text-base lg:text-lg">
                                        {item.title}
                                    </h3>
                                </div>

                                <p className=" text-gray-600 text-xs sm:text-sm leading-relaxedml-14 
                                   sm:ml-16">
                                    {item.desc}
                                </p>
                            </motion.div>
                        ))}
                    </motion.div>
                </motion.div>
            </div>
        </section>
    );
};

export default Services;
