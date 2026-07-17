import React from "react";
import logo from "../assets/logow.png";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

//Animation Variants
const fadeUp = {
    hidden: { opacity: 0, y: 50 },
    show: { opacity: 1, y: 0, transition: { duration: 1 } }
};

const stagger = {
    hidden: {},
    show: { transition: { staggerChildren: 0.2 } }
};

const Footer = () => {
    const { t } = useTranslation();

    return (
        <motion.footer
            variants={fadeUp}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
            className="w-full bg-[#0C111D] text-white px-6 lg:px-20 py-14">

            {/* MAIN CONTENT */}
            <motion.div
                variants={stagger}
                className="grid grid-cols-1 lg:grid-cols-3 gap-10">

                {/* LEFT SIDE */}
                <motion.div variants={fadeUp} className="flex flex-col gap-4">
                    <img src={logo} alt="logo" className="w-36" />

                    <p className="text-gray-400 leading-relaxed text-sm">
                        {t("footer_desc1")}
                    </p>

                    <p className="text-gray-400 leading-relaxed text-sm">
                        {t("footer_desc2")}
                    </p>
                </motion.div>

                <motion.div variants={fadeUp}></motion.div>

                {/* RIGHT SIDE */}
                <motion.div variants={fadeUp} className="flex flex-col gap-4">
                    <h3 className="text-white text-lg font-semibold">
                        {t("footer_download_title")}
                    </h3>

                    <div className="flex flex-wrap gap-4">
                        <a href="#" target="_blank">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg"
                                alt="Google Play" className="h-14"
                            />
                        </a>

                        <a href="#" target="_blank">
                            <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg"
                                alt="App Store" className="h-14"
                            />
                        </a>
                    </div>
                </motion.div>
            </motion.div>

            <motion.div
                variants={fadeUp}
                className="border-t border-gray-700 mt-10 pt-4 flex justify-between text-gray-500 text-sm">
                <p>{t("footer_bottom_left")}</p>
                <p>{t("footer_bottom_right")}</p>
            </motion.div>

        </motion.footer>
    );
};

export default Footer;
