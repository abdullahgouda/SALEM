import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import { signup } from "../../api/auth_api";

import {
    error as swalError,
    success as swalSuccess,
} from "../../utils/swal";

function Signup() {

    const { t, i18n } = useTranslation();

    const isArabic = i18n.language === "ar";

    const navigate = useNavigate();

    const [name, setName] = useState("");
    const [nationalId, setNationalId] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [department, setDepartment] = useState("");
    const [region, setRegion] = useState("");
    const [role, setRole] = useState("");

    const handleSubmit = async (e) => {

        e.preventDefault();

        const payload = {
            Name: name,
            National_Id: nationalId,
            Phone_Number: phoneNumber,
            Email: email,
            Password: password,
            User_Type: "employee",
            Role: role,
            Region: region,
            Department: department,
            Account_Status: "نشط",
        };

        try {

            await signup(payload);

            await swalSuccess(
                t("signupSuccess"),
                t("signupSuccessDesc")
            );

            navigate("/login");

        } catch (err) {

            const msg =
                err.response?.data?.detail ||
                err.response?.data?.message ||
                Object.values(err.response?.data || {})?.[0]?.[0] ||
                t("signupFailed");

            swalError(
                t("signupFailed"),
                typeof msg === "string"
                    ? msg
                    : JSON.stringify(msg)
            );
        }
    };

    return (
        <motion.div
            dir={isArabic ? "rtl" : "ltr"}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
                duration: 0.25,
                ease: [0.4, 0, 0.2, 1],
            }}
        >

            <h2 className="text-2xl font-extrabold text-gray-800 mb-6">
                {t("signupTitle")}
            </h2>

            <form
                onSubmit={handleSubmit}
                className="space-y-5 text-sm"
            >

                <input
                    type="text"
                    placeholder={t("fullName")}
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-3 py-2 border rounded-md"
                />

                <input
                    type="text"
                    maxLength={14}
                    placeholder={t("nationalId")}
                    value={nationalId}
                    onChange={(e) =>
                        setNationalId(e.target.value)
                    }
                    className="w-full px-3 py-2 border rounded-md"
                />

                <input
                    type="text"
                    placeholder={t("phoneNumber")}
                    value={phoneNumber}
                    onChange={(e) =>
                        setPhoneNumber(e.target.value)
                    }
                    className="w-full px-3 py-2 border rounded-md"
                />

                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder={t("email")}
                    className="w-full px-3 py-2 border rounded-md"
                />

                <input
                    type="password"
                    placeholder={t("password")}
                    value={password}
                    onChange={(e) =>
                        setPassword(e.target.value)
                    }
                    className="w-full px-3 py-2 border rounded-md"
                />

                {/* ROLE */}
                <select
    value={role}
    onChange={(e) => setRole(e.target.value)}
    className="w-full px-3 py-2 border rounded-md bg-white"
>
    <option value="">
        {t("selectRole")}
    </option>

    <option value="admin">
        {t("admin")}
    </option>

    <option value="operator">
        {t("employee")}
    </option>

    <option value="technical">
        {t("fieldWorker")}
    </option>

    <option value="supervisior">
        {t("distributionOfficer")}
    </option>
</select>

                {/* REGION */}
                <select
                    value={region}
                    onChange={(e) => setRegion(e.target.value)}
                    className="w-full px-3 py-2 border rounded-md bg-white"
                >
                    <option value="">
                        {t("region")}
                    </option>

                    <option value="Cairo">
                        Cairo
                    </option>

                    <option value="Giza">
                        Giza
                    </option>

                    <option value="Alexandria">
                        Alexandria
                    </option>
                </select>

                {/* DEPARTMENT */}
                <select
                    value={department}
                    onChange={(e) =>
                        setDepartment(e.target.value)
                    }
                    className="w-full px-3 py-2 border rounded-md bg-white"
                >
                    <option value="">
                        {t("department")}
                    </option>

                    <option value="gas">
                        Gas
                    </option>

                    <option value="water">
                        Water
                    </option>

                    <option value="electricity">
                        Electricity
                    </option>
                </select>

                <motion.button
                    type="submit"
                    whileHover={{ scale: 1.015 }}
                    whileTap={{ scale: 0.98 }}
                    className="
                        w-full py-2.5 rounded-xl
                        text-white font-semibold
                        bg-gradient-to-r
                        from-[#00816F]
                        to-[#2DDBC9]
                    "
                >
                    {t("signup")}
                </motion.button>

            </form>
        </motion.div>
    );
}

export default Signup;