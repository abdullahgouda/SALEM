import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import ReportsFilters from "./ReportsFilters";
import ReportsTableHeader from "./ReportsTableHeader";
import ReportsTableRows from "./ReportsTableRows";
import EmptyState from "./EmptyState";
import ReportDetailsPage from "./ReportDetailsPage";
import ReportMapPage from "./ReportMapPage";
import {
  getReports,
  getReportById,
  getDepartments,
  getIncidentStatuses,
} from "../../api/reports_api";

function ReportsPage() {
    const { t } = useTranslation();
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [departments, setDepartments] = useState([]);
    const [statuses, setStatuses] = useState([]);

    /* ===== Filters State ===== */
    const [searchId, setSearchId] = useState("");
    const [selectedDate, setSelectedDate] = useState(null);
    const [selectedDepartmentId, setSelectedDepartmentId] = useState("");
    const [selectedStatus, setSelectedStatus] = useState("");

    useEffect(() => {
        getDepartments().then((d) => setDepartments(Array.isArray(d) ? d : d?.results ?? []));
        getIncidentStatuses().then((s) => setStatuses(Array.isArray(s) ? s : s?.results ?? []));
    }, []);

    useEffect(() => {
        let cancelled = false;
        queueMicrotask(() => { if (!cancelled) setLoading(true); });
        const dateFrom = selectedDate ? `${selectedDate.getFullYear()}-${String(selectedDate.getMonth() + 1).padStart(2, "0")}-${String(selectedDate.getDate()).padStart(2, "0")}` : "";
        getReports({
            search: searchId.trim() || undefined,
            status: selectedStatus || undefined,
            department: selectedDepartmentId || undefined,
            dateFrom: dateFrom || undefined,
            dateTo: undefined,
        }).then((data) => {
            if (!cancelled) {
                setReports(data ?? []);
                setPage(1);
                setLoading(false);
            }
        }).catch(() => { if (!cancelled) setLoading(false); });
        return () => { cancelled = true; };
    }, [searchId, selectedStatus, selectedDepartmentId, selectedDate]);

    /* ========= Reports from API are already filtered ========= */
    const filteredReports = reports;

    /* ===== Pagination ===== */
    const rowsPerPage = 12;
    const totalPages = Math.max(1, Math.ceil(filteredReports.length / rowsPerPage));

    /* ===== Details Modal ===== */
    const [openDetails, setOpenDetails] = useState(false);
    const [showMap, setShowMap] = useState(false);
    const [selectedReport, setSelectedReport] = useState(null);
    const [detailLoading, setDetailLoading] = useState(false);

    /* ========= Pagination ========= */
    const startIndex = (page - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const visibleReports = filteredReports.slice(startIndex, endIndex);
    const hasData = filteredReports.length > 0;

    return (
        <>
            <div className={`px-6 py-4 ${openDetails ? "blur-sm" : ""}`}>
                <ReportsFilters
                    departments={departments}
                    statuses={statuses}
                    onSearchChange={setSearchId}
                    onDateChange={setSelectedDate}
                    onDepartmentChange={setSelectedDepartmentId}
                    onStatusChange={setSelectedStatus}
                />

                <div className="mt-4">
                    <ReportsTableHeader />

                    {loading ? (
                        <p className="py-8 text-center text-gray-500">{t("loading") || "Loading..."}</p>
                    ) : hasData ? (
                        <>
                            <ReportsTableRows
                                reports={visibleReports}
                                onView={async (report) => {
                                    setShowMap(false);
                                    setOpenDetails(true);
                                    setSelectedReport(null);
                                    setDetailLoading(true);
                                    try {
                                        const full = await getReportById(report.id);
                                        setSelectedReport(full ?? report);
                                    } catch {
                                        setSelectedReport(report);
                                    }
                                    setDetailLoading(false);
                                }}
                            />

                            <div className="flex justify-between items-center mt-4 text-sm">
                                <span className="text-gray-500">
                                    {t("page")} {page} {t("of")} {totalPages}
                                </span>

                                <div className="flex gap-2">
                                    <button
                                        disabled={page === 1}
                                        onClick={() => setPage((p) => Math.max(p - 1, 1))}
                                        className="px-3 py-1 rounded-lg border disabled:opacity-40">
                                        {t("previous")}
                                    </button>

                                    <button
                                        disabled={page === totalPages}
                                        onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
                                        className="px-3 py-1 rounded-lg border disabled:opacity-40">
                                        {t("next")}
                                    </button>
                                </div>
                            </div>
                        </>
                    ) : (
                        <EmptyState />
                    )}
                </div>
            </div>

            {openDetails && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
                    <div className="absolute inset-0 backdrop-blur-sm"></div>

                    <div className="relative bg-white w-[90%] max-w-6xl h-[85vh] rounded-2xl p-6">
                        <button
                            onClick={() => {
                                setOpenDetails(false);
                                setShowMap(false);
                            }}
                            className="absolute top-4 left-4 text-green-800 text-xl font-bold" >
                            ✕
                        </button>

                        {!showMap ? (
                            detailLoading ? (
                                <p className="py-12 text-center text-gray-500">{t("loading") || "Loading..."}</p>
                            ) : (
                                <ReportDetailsPage
                                    report={selectedReport}
                                    onOpenMap={() => setShowMap(true)}
                                />
                            )
                        ) : (
                            <ReportMapPage
                                location={selectedReport?.location}
                                onBack={() => setShowMap(false)}
                            />
                        )}
                    </div>
                </div>
            )}
        </>
    );
}

export default ReportsPage;
