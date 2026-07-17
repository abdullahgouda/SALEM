import { useTranslation } from "react-i18next";

export default function StreetsHistoryMap({ location, onBack }) {
    const { t, i18n } = useTranslation();
    const isArabic = i18n.language === "ar";

    const mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(
        location || "Cairo"
    )}&output=embed`;

    return (
        <div
            dir={isArabic ? "rtl" : "ltr"}
            className="h-full flex flex-col">
            <h2 className="text-lg font-bold text-center mb-4">
                {t("mapTitleWithLocation", { location })}
            </h2>

            <div className="flex-1 rounded-xl overflow-hidden border">
                <iframe
                    title="map"
                    src={mapUrl}
                    className="w-full h-full"
                    loading="lazy"
                />
            </div>

            <div className="mt-6 flex justify-center">
                <button
                    onClick={onBack}
                    className="px-6 py-2 border border-red-500 text-red-500 rounded-lg">
                    {t("back")}
                </button>
            </div>
        </div>
    );
}
