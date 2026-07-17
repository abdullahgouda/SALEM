import Swal from "sweetalert2";

const isRTL = () => typeof window !== "undefined" && localStorage.getItem("lang") === "ar";

const defaultOptions = () => ({
    confirmButtonColor: "#00816F",
    cancelButtonColor: "#6b7280",
    customClass: {
        popup: isRTL() ? "swal2-rtl" : "",
        title: isRTL() ? "swal2-rtl" : "",
        htmlContainer: isRTL() ? "swal2-rtl" : "",
        confirmButton: isRTL() ? "swal2-rtl" : "",
        cancelButton: isRTL() ? "swal2-rtl" : "",
    },
});

export const toast = (options = {}) => {
    return Swal.fire({
        toast: true,
        position: isRTL() ? "top-start" : "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toastEl) => {
            toastEl.onmouseenter = Swal.stopTimer;
            toastEl.onmouseleave = Swal.resumeTimer;
        },
        ...defaultOptions(),
        ...options,
    });
};

export const success = (title, text) => {
    return Swal.fire({
        icon: "success",
        title: title ?? "Success",
        text: text ?? "",
        ...defaultOptions(),
    });
};

export const error = (title, text) => {
    return Swal.fire({
        icon: "error",
        title: title ?? "Error",
        text: text ?? "",
        ...defaultOptions(),
    });
};

export const confirm = (options = {}) => {
    return Swal.fire({
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: options.confirmText ?? "Confirm",
        cancelButtonText: options.cancelText ?? "Cancel",
        ...defaultOptions(),
        ...options,
    });
};

export default Swal;
