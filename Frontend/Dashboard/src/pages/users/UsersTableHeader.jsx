import { useTranslation } from "react-i18next";

function UsersTableHeader() {

    const { t } = useTranslation();

    return (
        <div
            className="
                min-w-[900px]
                mt-4
                bg-gradient-to-r from-[#00816F] to-[#2DDBC9]
                text-white
                rounded-xl
                px-4 py-3
                text-sm font-semibold
            "
        >
            <div className="grid grid-cols-6 items-center text-center">

                <div>{t("name")}</div>

                <div>{t("email")}</div>

                <div>{t("rolePermission")}</div>

                <div>{t("status")}</div>

                <div>{t("lastLogin")}</div>

                <div>{t("procedures")}</div>

            </div>
        </div>
    );
}

export default UsersTableHeader;