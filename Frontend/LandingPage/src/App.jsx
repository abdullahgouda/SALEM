import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Home from "./components/Home";
import LiveState from "./components/LiveState";
import Services from "./components/Services";
import DownloadApp from "./components/DownloadApp";
import Contact from "./components/Contact";
import Footer from "./components/Footer";

export default function App() {
  const { i18n } = useTranslation();

  //  RTL / LTR
  useEffect(() => {
    if (i18n.language === "ar") {
      document.documentElement.dir = "rtl";
      document.documentElement.lang = "ar";
    } else {
      document.documentElement.dir = "ltr";
      document.documentElement.lang = "en";
    }
  }, [i18n.language]);

  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang);
  };

  return (
    <>
      <ToastContainer position="top-right" />
      <Home changeLanguage={changeLanguage} />
      <LiveState />
      <Services />
      <DownloadApp />
      <Contact />
      <Footer />
    </>
  );
}
