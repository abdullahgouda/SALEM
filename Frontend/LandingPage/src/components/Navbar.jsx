import React, { useEffect, useState } from 'react';
import { assets } from '../assets/assets';
import { useTranslation } from "react-i18next";

// تحديد رابط الـ Dashboard
const DASHBOARD_URL = import.meta.env.VITE_DASHBOARD_URL || "https://dashboardsalem-psi.vercel.app";

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

    // دالة التوجيه لصفحة تسجيل الدخول
    const handleGoToLogin = (e) => {
        e.preventDefault();
        window.location.href = `${DASHBOARD_URL}/login`;
    };

    // دالة التوجيه المباشر للـ Dashboard الرئيسية
    const handleGoToDashboard = (e) => {
        e.preventDefault();
        window.location.href = DASHBOARD_URL;
    };

    return (
        <div className="absolute top-0 left-0 w-full z-50">
            <div className="container mx-auto flex justify-between items-center py-4 px-6 md:px-20 lg:px-32">

                <img src={assets.logow} className="w-24" alt="logo" />

                {/* Links */}
                <ul className="hidden md:flex gap-7 text-white items-center">
                    <a href="#Home" className="hover:text-gray-300">{t("nav_home")}</a>
                    <a href="#LiveState" className="hover:text-gray-300">{t("nav_live")}</a>
                    <a href="#Services" className="hover:text-gray-300">{t("nav_services")}</a>
                    <a href="#DownloadApp" className="hover:text-gray-300">{t("nav_download")}</a>
                    <a href="#Contact" className="hover:text-gray-300">{t("nav_contact")}</a>
                </ul>

                {/* Actions (Lang + Dashboard + Login) - Desktop */}
                <div className="hidden md:flex items-center gap-3">
                    <button onClick={toggleLang}
                        className="px-3 py-2 text-white hover:text-gray-300 transition">
                        {nextLang}
                    </button>

                    {/* زر الذهاب للـ Dashboard */}
                    <button 
                        onClick={handleGoToDashboard}
                        className="px-4 py-2 text-white border border-[#00BE9B] hover:bg-[#00BE9B] rounded-xl font-medium transition-all duration-300 shadow-md cursor-pointer">
                        {t("dashboard") || "لوحة التحكم"}
                    </button>

                    {/* زر تسجيل الدخول */}
                    <button 
                        onClick={handleGoToLogin}
                        className="px-4 py-2 text-white bg-[#00BE9B] hover:bg-[#00a385] rounded-xl font-medium transition-all duration-300 shadow-md cursor-pointer">
                        {t("login") || "تسجيل الدخول"}
                    </button>
                </div>

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

                    {/* زرار الـ Dashboard في الموبايل */}
                    <button 
                        onClick={(e) => { setMobileMenu(false); handleGoToDashboard(e); }}
                        className="mt-2 px-6 py-2 border-2 border-[#00BE9B] text-[#00BE9B] font-semibold rounded-lg cursor-pointer">
                        {t("dashboard") || "لوحة التحكم"}
                    </button>

                    {/* زرار اللوجن في الموبايل */}
                    <button 
                        onClick={(e) => { setMobileMenu(false); handleGoToLogin(e); }}
                        className="px-6 py-2 bg-[#00BE9B] text-white rounded-lg cursor-pointer">
                        {t("login") || "تسجيل الدخول"}
                    </button>

                    {/* Change lang inside mobile */}
                    <button onClick={() => { toggleLang(); setMobileMenu(false); }}
                        className="px-6 py-2 bg-black text-white rounded">
                        {nextLang}
                    </button>
                </ul>

            </div>
        </div>
    );
};

export default Navbar;