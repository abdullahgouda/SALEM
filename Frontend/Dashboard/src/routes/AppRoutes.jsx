import { Routes, Route } from "react-router-dom";

import AuthLayout from "../layout/AuthLayout";
import DashboardLayout from "../layout/DashboardLayout";

import Login from "../pages/auth/Login";

import ForgetPassword from "../pages/auth/ForgetPassword";
import Verification from "../pages/auth/Verification";
import SetNewPassword from "../pages/auth/SetNewPassword";

import HomePage from "../pages/home/HomePage";
import ReportsPage from "../pages/reports/ReportsPage";
import WorkflowPage from "../pages/workflow/WorkflowPage";
import StreetsHistoryPage from "../pages/streetsHistory/StreetsHistoryPage";
import StatisticsPage from "../pages/statistics/StatisticsPage";
import NotificationsPage from "../pages/notifications/NotificationsPage";
import UsersPage from "../pages/users/UsersPage";
import Signup from "../pages/users/Signup";
import AddUserPage from "../pages/users/AddUserPage";
import SettingsPage from "../pages/settings/SettingsPage";





function AppRoutes() {
    return (
        <Routes>

            {/* ========== Auth ========== */}
            <Route element={<AuthLayout />}>
                <Route path="/" element={<Login />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/forget-password" element={<ForgetPassword />} />
                <Route path="/verification" element={<Verification />} />
                <Route path="/set-new-password" element={<SetNewPassword />} />
            </Route>

            {/* ========== Dashboard ========== */}
            <Route element={<DashboardLayout />}>
                <Route path="/dashboard" element={<HomePage />} />
                <Route path="/dashboard/reports" element={<ReportsPage />} />
                <Route path="/dashboard/workflow" element={<WorkflowPage />} />
                <Route path="/dashboard/streets-history" element={<StreetsHistoryPage/>} />
                <Route path="/dashboard/statistics" element={<StatisticsPage />} />
                <Route path="/dashboard/notifications" element={<NotificationsPage />}/>
                <Route path="/dashboard/users" element={<UsersPage/>} />
                <Route path="/dashboard/users/add" element={<AddUserPage />} />
                <Route path="/dashboard/settings" element={<SettingsPage />} />
            </Route>

        </Routes>
    );
}

export default AppRoutes;
