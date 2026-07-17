import { useTranslation } from "react-i18next";
import avatar from "../../assets/avatar.png";

export default function StreetsHistoryDetails({ report, onOpenMap }) {
  const { t, i18n } = useTranslation();
  const isArabic = i18n.language === "ar";

  if (!report) return null;

  return (
    <div
      dir={isArabic ? "rtl" : "ltr"}
      className="h-full flex flex-col px-6 py-4 bg-white rounded-xl">
      {/* ===== TITLE ===== */}
      <h2 className="text-lg font-bold text-center mb-4">
        {t("procedures")}
      </h2>

      {/* ===== CONTENT ===== */}
      <div className="flex-1 grid grid-cols-12 gap-6">
        {/* ===== LEFT ===== */}
        <div className="col-span-7 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <ImageCard title={t("after")} />
            <ImageCard title={t("before")} />
          </div>

          <TextArea
            label={t("aiInitialAnalysis")}
            value={`${t("aiInitial")} ${t(report.category)}`}
          />

          <TextArea
            label={t("aiComparisonResult")}
            value={t("aiNoChange")}
          />
        </div>

        {/* ===== RIGHT ===== */}
        <div className="col-span-5 space-y-3">
          <Field label={t("reportNumberLabel")} value={report.id} />
          <Field label={t("problemTypeLabel")} value={t(report.category)} />
          <Field label={t("registrationDate")} value={report.date} />
          <Field label={t("status")} value={t(report.status)} />
          <Field label={t("repairTime")} value={t(report.repairTime)} />
          <Field label={t("responsibleEntity")} value={t(report.process)} />
        </div>
      </div>

      {/* ===== ACTION ===== */}
      <div className="mt-4 pt-4 border-t flex justify-center">
        <button
          onClick={onOpenMap}
          className="px-4 py-2 bg-gradient-to-r from-[#00816F] to-[#2DDBC9] text-white rounded-lg text-sm">
          {t("showOnMap")}
        </button>
      </div>
    </div>
  );
}

/* ================= Components ================= */

function Field({ label, value }) {
  return (
    <div>
      <label className="block text-xs font-medium text-gray-700 mb-1">
        {label}
      </label>
      <input
        disabled
        value={value ?? "—"}
        className="w-full rounded-md border px-2 py-1 text-sm bg-gray-50"
      />
    </div>
  );
}

function ImageCard({ title }) {
  return (
    <div className="text-center">
      <p className="mb-1 text-sm font-medium text-gray-700">
        {title}
      </p>
      <img
        src={avatar}
        alt={title}
        className="w-full h-44 object-cover rounded-lg border"
      />
    </div>
  );
}

function TextArea({ label, value }) {
  return (
    <div>
      <label className="block text-xs font-medium text-gray-700 mb-1">
        {label}
      </label>
      <textarea
        disabled
        value={value}
        className="w-full h-20 rounded-md border p-2 text-sm bg-gray-50 resize-none"
      />
    </div>
  );
}
