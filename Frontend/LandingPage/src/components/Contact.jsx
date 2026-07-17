import React, { useState } from "react";
import { FaMapMarkerAlt, FaEnvelope, FaPhone } from "react-icons/fa";
import { motion } from "framer-motion";
import { toast } from "react-toastify";
import { useTranslation } from "react-i18next";

/* ================= Animations ================= */
const fadeUp = {
    hidden: { opacity: 0, y: 60 },
    show: { opacity: 1, y: 0, transition: { duration: 1 } }
};

const fadeLeft = {
    hidden: { opacity: 0, x: 60 },
    show: { opacity: 1, x: 0, transition: { duration: 1 } }
};

const fadeRight = {
    hidden: { opacity: 0, x: -60 },
    show: { opacity: 1, x: 0, transition: { duration: 1 } }
};

const stagger = {
    hidden: {},
    show: { transition: { staggerChildren: 0.15 } }
};

const Contact = () => {
    const { t } = useTranslation();
    const [result, setResult] = useState("");

    const onSubmit = async (event) => {
        event.preventDefault();
        setResult(t("contact_sending"));

        const formData = new FormData(event.target);
        formData.append("access_key", "a85d41b3-5f88-41fc-8056-109bcfb02cea");

        const response = await fetch("https://api.web3forms.com/submit", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (data.success) {
            toast.success(t("contact_success"));
            setResult("");
            event.target.reset();
        } else {
            toast.error(t("contact_error"));
            setResult("");
        }
    };

    return (
        <div id="Contact"
             className="w-full min-h-screen py-24 px-6 lg:px-20 flex justify-center items-start bg-white">
            <motion.div
                variants={fadeUp}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true }}
                className="w-full max-w-7xl bg-white shadow-xl rounded-2xl p-10 lg:p-14 border border-gray-200">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-14">

                    {/* ================= FORM ================= */}
                    <motion.form
                        onSubmit={onSubmit}
                        variants={stagger}
                        initial="hidden"
                        whileInView="show"
                        viewport={{ once: true }}
                        className="flex flex-col gap-6">

                        <motion.input
                            variants={fadeRight} type="text"name="name"
                            placeholder={t("contact_name")} required
                            className="w-full border border-gray-300 rounded-lg p-4 text-gray-700 outline-none
                            transition hover:border-[#1B4374] focus:border-[#1B4374]"
                        />

                        <motion.input
                            variants={fadeRight} type="email"name="email"
                            placeholder={t("contact_email_input")} required
                            className="w-full border border-gray-300 rounded-lg p-4 text-gray-700 outline-none transition
                             hover:border-[#1B4374]focus:border-[#1B4374]"
                        />

                        <motion.input
                            variants={fadeRight} type="text" name="subject"
                            placeholder={t("contact_subject")} required
                            className="w-full border border-gray-300 rounded-lg p-4 text-gray-700 outline-none 
                            transition hover:border-[#1B4374] focus:border-[#1B4374]"
                        />

                        <motion.textarea
                            variants={fadeRight} name="message"
                            placeholder={t("contact_message")}required
                            className="w-full border border-gray-300 rounded-lg p-4 h-40 text-gray-700 outline-none resize-none
                            transition hover:border-[#1B4374] focus:border-[#1B4374]"
                        />

                        {/* ===== SUBMIT BUTTON (hover شغال صح) ===== */}
                        <motion.button
                            variants={fadeUp}
                            type="submit"
                            whileHover={{ scale: 1.05, opacity: 0.9 }}
                            whileTap={{ scale: 0.97 }}
                            transition={{ duration: 0.2 }}
                            className=" w-40 text-white py-3 rounded-lg bg-gradient-to-r from-[#00BE9B] to-[#1B4374]"
                        >
                            {result ? result : t("contact_send")}
                        </motion.button>
                    </motion.form>

                    {/* ================= INFO ================= */}
                    <motion.div
                        variants={fadeLeft}
                        initial="hidden"
                        whileInView="show"
                        viewport={{ once: true }}
                        className="flex flex-col gap-6">
                        <h3 className="text-2xl font-bold">{t("contact_title")}</h3>

                        <p className="text-gray-600 leading-relaxed">
                            {t("contact_desc")}
                        </p>

                        <div className="flex items-start gap-4">
                            <FaMapMarkerAlt className="text-[#1B4374] text-2xl mt-1" />
                            <p className="text-gray-700">{t("contact_address")}</p>
                        </div>

                        <div className="flex items-start gap-4">
                            <FaEnvelope className="text-[#1B4374] text-2xl mt-1" />
                            <p className="text-gray-700">
                                salemproject75cs@gmail.com
                            </p>
                        </div>

                        <div className="flex items-start gap-4">
                            <FaPhone className="text-[#1B4374] text-2xl mt-1" />
                            <p className="text-gray-700">
                                +20 100 000 0000
                            </p>
                        </div>
                    </motion.div>

                </div>
            </motion.div>
        </div>
    );
};

export default Contact;
