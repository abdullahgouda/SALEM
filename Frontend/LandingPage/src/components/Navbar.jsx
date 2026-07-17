import React, { useEffect, useState } from 'react';
import { assets } from '../assets/assets';
import { useTranslation } from "react-i18next";

const Navbar = ({ changeLanguage }) => {

    const { t, i18n } = useTranslation();

    const [showMobileMenu, setMobileMenu] = useState(false);

    useEffect(() => {
        document.body.style.overflow = showMobileMenu ? 'hidden' : 'auto';
    }, [showMobileMenu]);

    // Lang
    const nextLang = i18n.language === "ar" ? "EN" : "AR";


    const toggleLang = () => {
        const newLang = i18n.language === "ar" ? "en" : "ar";
        changeLanguage(newLang); 
    };

    return (
        <div className="absolute top-0 left-0 w-full z-50">
            <div className="container mx-auto flex justify-between items-center py-4 px-6 md:px-20 lg:px-32">

                <img src={assets.logow} className="w-24" alt="logo" />

                {/* Links */}
                <ul className="hidden md:flex gap-7 text-white">
                    <a href="#Home" className="hover:text-gray-300">{t("nav_home")}</a>
                    <a href="#LiveState" className="hover:text-gray-300">{t("nav_live")}</a>
                    <a href="#Services" className="hover:text-gray-300">{t("nav_services")}</a>
                    <a href="#DownloadApp" className="hover:text-gray-300">{t("nav_download")}</a>
                    <a href="#Contact" className="hover:text-gray-300">{t("nav_contact")}</a>
                </ul>

                {/* Lang Button */}
                <button onClick={toggleLang}
                    className="hidden md:block px-6 py-2 text-white hover:text-gray-300">
                    {nextLang}
                </button>

                {/* Mobile menu icon */}
                <img src={assets.menu_icon} onClick={() => setMobileMenu(true)}
                    className="md:hidden w-7 cursor-pointer" alt="menu"
                />
            </div>

            {/* Mobile Menu */}
            <div className={`${showMobileMenu ? "fixed w-full" : "h-0 w-0"} top-0 right-0 bottom-0 bg-white overflow-hidden transition-all md:hidden`}>

                <div className="flex justify-end p-6 cursor-pointer">
                    <img src={assets.cross_icon} onClick={() => setMobileMenu(false)}
                        className="w-6" alt="close"
                    />
                </div>

                <ul className="flex flex-col gap-3 items-center text-lg font-medium">
                    <a href="#Home" onClick={() => setMobileMenu(false)}>{t("nav_home")}</a>
                    <a href="#LiveState" onClick={() => setMobileMenu(false)}>{t("nav_live")}</a>
                    <a href="#Services" onClick={() => setMobileMenu(false)}>{t("nav_services")}</a>
                    <a href="#DownloadApp" onClick={() => setMobileMenu(false)}>{t("nav_download")}</a>
                    <a href="#Contact" onClick={() => setMobileMenu(false)}>{t("nav_contact")}</a>

                    {/* Change lan inside mobible */}
                    <button onClick={() => { toggleLang(); setMobileMenu(false); }}
                        className="mt-4 px-6 py-2 bg-black text-white rounded">
                        {nextLang}
                    </button>
                </ul>

            </div>
        </div>
    );
};

export default Navbar;
