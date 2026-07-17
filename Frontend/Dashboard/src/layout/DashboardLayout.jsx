import { Outlet, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useState } from "react";
import Sidebar from "../components/common/Sidebar";
import Header from "../components/common/Header";
import { logout } from "../api/auth_api";

function DashboardLayout() {
    const navigate = useNavigate();
    const { i18n } = useTranslation();
    const [openSidebar, setOpenSidebar] = useState(false);

    const handleLogout = async () => {
        await logout();
        navigate("/login", { replace: true });
    };

    return (
        <div
            className={`flex min-h-screen bg-[#F6F7FB] ${i18n.language === "ar"
                    ? "flex-row"
                : "flex-row-reverse"
                }`}
        >
            {/* Sidebar في الديسكتوب فقط */}
            <div className="hidden lg:block">
                <Sidebar />
            </div>

            {/* المحتوى */}
            <div className="flex-1 flex flex-col">
                <Header
                    onLogout={handleLogout}
                    onMenuClick={() => setOpenSidebar(true)}
                />

                <main className="flex-1 p-4 sm:p-6 overflow-x-hidden min-w-0">
                    <Outlet />
                </main>
            </div>

            {/* ===== Sidebar Overlay للموبايل ===== */}
            {openSidebar && (
                <>
                    {/* الخلفية */}
                    <div
                        className="fixed inset-0 bg-black/40 z-40 lg:hidden"
                        onClick={() => setOpenSidebar(false)}
                    />

                    {/* السايدبار */}
                    <div
                        className={`fixed top-0 ${i18n.language === "ar"
                                ? "right-0"
                                : "left-0"
                            } h-full w-64 bg-white z-50 lg:hidden`}
                    >
                        <Sidebar />
                    </div>
                </>
            )}
        </div>
    );
}

export default DashboardLayout;
