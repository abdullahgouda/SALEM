import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

export default function EditUserModal({
    user,
    onClose,
    onSave,
}) {

    const { t } = useTranslation();

    const [form, setForm] = useState({
        oldPassword: "",
        newPassword: "",
        confirmPassword: "",
        role: "",
    });

    useEffect(() => {

        if (user) {

            setForm({
                oldPassword: "",
                newPassword: "",
                confirmPassword: "",
                role: user.role || "",
            });
        }

    }, [user]);

    const handleSubmit = () => {

        if (
            form.newPassword !==
            form.confirmPassword
        ) {
            alert(t("passwordsNotMatch"));
            return;
        }

        onSave?.(form);
    };

    if (!user) return null;

    return (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">

            <div className="absolute inset-0 backdrop-blur-sm"></div>

            {/* BOX */}
            <div className="relative bg-white w-[92%] md:w-[850px] rounded-2xl shadow-2xl px-5 py-5">

                {/* TITLE */}
                <h2 className="text-xl font-bold text-center mb-6">
                    {t("editEmployeeTitle")}
                </h2>

                {/* FORM */}
                <div className="space-y-5">

                    {/* OLD PASSWORD */}
                    <div>
                        <label className="block text-sm font-semibold text-[#163C4A] mb-2">
                            {t("oldPassword")}
                        </label>

                        <input
                            type="password"
                            placeholder={t("enterPasswordHere")}
                            value={form.oldPassword}
                            onChange={(e) =>
                                setForm({
                                    ...form,
                                    oldPassword:
                                        e.target.value,
                                })
                            }
                            className="w-full h-11 rounded-xl border border-gray-200 px-4 text-sm outline-none"
                        />
                    </div>

                    {/* NEW PASSWORD */}
                    <div>
                        <label className="block text-sm font-semibold text-[#163C4A] mb-2">
                            {t("newPassword")}
                        </label>

                        <input
                            type="password"
                            placeholder={t("enterPasswordHere")}
                            value={form.newPassword}
                            onChange={(e) =>
                                setForm({
                                    ...form,
                                    newPassword:
                                        e.target.value,
                                })
                            }
                            className="w-full h-11 rounded-xl border border-gray-200 px-4 text-sm outline-none"
                        />
                    </div>

                    {/* CONFIRM PASSWORD */}
                    <div>
                        <label className="block text-sm font-semibold text-[#163C4A] mb-2">
                            {t("confirmNewPassword")}
                        </label>

                        <input
                            type="password"
                            placeholder={t("enterPasswordHere")}
                            value={
                                form.confirmPassword
                            }
                            onChange={(e) =>
                                setForm({
                                    ...form,
                                    confirmPassword:
                                        e.target.value,
                                })
                            }
                            className="w-full h-11 rounded-xl border border-gray-200 px-4 text-sm outline-none"
                        />
                    </div>

                    {/* ROLE */}
                    <div className="w-full md:w-[280px]">
                        <label className="block text-sm font-semibold text-[#163C4A] mb-2">
                            {t("requestRoleChange")}
                        </label>

                        <select
                            value={form.role}
                            onChange={(e) =>
                                setForm({
                                    ...form,
                                    role:
                                        e.target.value,
                                })
                            }
                            className="w-full h-11 rounded-xl border border-gray-200 px-4 text-sm outline-none bg-white"
                        >
                            <option value="">
                                {t("selectNextRole")}
                            </option>

                            <option>
                                {t("admin")}
                            </option>

                            <option>
                                {t("employee")}
                            </option>

                            <option>
                                {t("fieldWorker")}
                            </option>

                            <option>
                                {t("distributionOfficer")}
                            </option>
                        </select>
                    </div>
                </div>

                {/* BUTTONS */}
                <div className="mt-10 grid grid-cols-3 gap-4">

                    <button
                        onClick={onClose}
                        className="h-11 rounded-xl border border-red-500 text-red-500 font-bold text-sm"
                    >
                        {t("exit")}
                    </button>

                    <button
                        className="h-11 rounded-xl border border-red-500 text-red-500 font-bold text-sm"
                    >
                        {t("disableAccount")}
                    </button>

                    <button
                        onClick={handleSubmit}
                        className="h-11 rounded-xl text-white font-bold text-sm bg-gradient-to-r from-[#00816F] to-[#2DDBC9]"
                    >
                        {t("confirmChanges")}
                    </button>
                </div>
            </div>
        </div>
    );
}