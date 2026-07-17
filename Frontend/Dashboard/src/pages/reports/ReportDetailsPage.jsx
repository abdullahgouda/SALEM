import { useTranslation } from "react-i18next";
import placeholderImg from "../../assets/avatar.png";

export default function ReportDetailsPage({ report, onOpenMap }) {
  const { t, i18n } = useTranslation();
  const isArabic = i18n.language === "ar";

  if (!report) return null;

  return (
    <div dir={isArabic ? "rtl" : "ltr"} className="h-full flex flex-col px-6 py-4">

      {/* ===== TITLE ===== */}
      <h2 className="text-lg font-bold text-center mb-4">
        {t("reportDetails")}
      </h2>

      {/* ===== CONTENT ===== */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* ===== LEFT : IMAGES ===== */}
        <div className="lg:col-span-7 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <ImageCard title={t("before")} src={report.beforeImage} />
            <ImageCard title={t("after")} src={report.afterImage} />
          </div>

          <TextArea
            label={t("aiAnalysis")}
            value={report.aiAnalysis ? `${t("initialClassification")} ${report.aiAnalysis}` : `${t("initialClassification")} ${t(report.category)}`}
          />

          <TextArea
            label={t("aiComparison")}
            value={t("noChangeDetected")}
          />
        </div>

        {/* ===== RIGHT : DETAILS ===== */}
        <div className="lg:col-span-5 space-y-3">
          <Field label={t("reportNumber")} value={report.id} />
          <Field label={t("category")} value={t(report.category)} />
          <Field label={t("location")} value={t(report.location)} />
          <Field label={t("reportDate")} value={report.date} />
          <Field label={t("status")} value={t(report.status)} />
          <Field label={t("entity")} value={t(report.entity)} />
          <Field label={t("priority")} value={t(report.priority)} />
        </div>
      </div>

      {/* ===== ACTIONS ===== */}
      <div className="mt-4 pt-4 border-t flex justify-center">
        <div className="flex gap-4">
          <button
            onClick={onOpenMap}
            className="px-4 py-2 bg-gradient-to-r from-[#00816F] to-[#2DDBC9] text-white rounded-lg text-sm"
          >
            {t("showOnMap")}
          </button>
        </div>
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
        value={value ?? ""}
        className="w-full rounded-md border px-2 py-1 text-sm bg-gray-50"
      />
    </div>
  );
}

function ImageCard({ title, src }) {
  return (
    <div className="text-center">
      <p className="mb-1 text-sm font-medium text-gray-700">
        {title}
      </p>
      <img
        src={src || placeholderImg}
        alt={title}
        className="w-full h-64 object-contain rounded-lg border bg-gray-100"
        onError={(e) => { e.target.onerror = null; e.target.src = placeholderImg; }}
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
        className="w-full h-10 rounded-md border p-2 text-sm bg-gray-50 resize-none"
      />
    </div>
  );
}
