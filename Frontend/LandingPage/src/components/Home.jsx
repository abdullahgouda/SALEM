import React from "react";
import Navbar from "./Navbar";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

const Home = ({ changeLanguage }) => {
    const { t } = useTranslation();

    return (
        <section id="Home"
            className="relative min-h-screen bg-cover bg-center bg-no-repeat flex items-center"
            style={{ backgroundImage: "url('/background.png')" }}>
            <Navbar changeLanguage={changeLanguage} />

            {/* Overlay */}
            <div className="absolute inset-0 bg-black/50"></div>

            <div className="relative w-full text-center text-white px-6 sm:px-10 lg:px-32">
                <motion.div
                    initial={{ opacity: 0, y: 80 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1.2 }}>
                    {/* TITLE */}
                    <h2
                        className="mx-auto max-w-3xl font-semibold leading-tight text-2xl sm:text-3xl
                        md:text-5xl lg:text-[60px]">
                        {t("home_title")}
                    </h2>

                    {/* BUTTONS */}
                    <div
                        className="mt-12 flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center
                        items-center">
                        {/* Services Button */}
                        <a href="#Services"
                            className=" w-full sm:w-auto px-10 sm:px-14 lg:px-20 py-3 rounded-xl
                            text-sm sm:text-base lg:text-lg font-medium text-white bg-gradient-to-b from-[#00BE9B] to-[#1B4374]
                            text-center transition-all duration-300 ease-out hover:scale-105 hover:shadow-xl active:scale-95">
                            {t("our_services")}
                        </a>

                        {/* Download Button – حركة فقط */}
                        <a href="#DownloadApp"
                            className="w-full sm:w-auto px-10 sm:px-14 lg:px-20 py-3 rounded-xl text-sm sm:text-base lg:text-lg
                            font-medium border border-white text-white text-center transition-all duration-300 ease-out
                            hover:scale-105 hover:shadow-[0_10px_30px_rgba(255,255,255,0.15)] active:scale-95">
                            {t("download_app")}
                        </a>
                    </div>
                </motion.div>
            </div>
        </section>
    );
};

export default Home;
