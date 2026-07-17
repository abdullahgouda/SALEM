export const fadeUp = {
    hidden: { opacity: 0, y: 60 },
    show: {
        opacity: 1,
        y: 0,
        transition: { duration: 1, ease: "easeOut" }
    }
};

export const fadeLeft = {
    hidden: { opacity: 0, x: 60 },
    show: {
        opacity: 1,
        x: 0,
        transition: { duration: 1, ease: "easeOut" }
    }
};

export const fadeRight = {
    hidden: { opacity: 0, x: -60 },
    show: {
        opacity: 1,
        x: 0,
        transition: { duration: 1, ease: "easeOut" }
    }
};

export const fadeScale = {
    hidden: { opacity: 0, scale: 0.8 },
    show: {
        opacity: 1,
        scale: 1,
        transition: { duration: 1, ease: "easeOut" }
    }
};

export const stagger = {
    hidden: {},
    show: {
        transition: {
            staggerChildren: 0.2
        }
    }
};
