// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brandTop: "#00BE9B",
        brandBottom: "#1B4374",
        darkBg: "#0C111D",
      },
      backgroundImage: {
        'diagonal-pattern': `repeating-linear-gradient(135deg, rgba(255,255,255,0.02) 0 16px, transparent 16px 32px)`,
      }
    },
  },
  plugins: [],
}
