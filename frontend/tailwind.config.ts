import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        rail: {
          bg: "#080c14",
          panel: "#101827",
          panelSoft: "#131f33",
          text: "#d8e4ff",
          muted: "#8fa5cc",
          accent: "#15c2a4",
          warning: "#f7b955",
          danger: "#ff6b6b"
        },
      },
      boxShadow: {
        card: "0 15px 40px rgba(7, 13, 25, 0.45)",
      },
      fontFamily: {
        sans: ["var(--font-sans)"],
      },
    },
  },
  plugins: [],
};

export default config;
