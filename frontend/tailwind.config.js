/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        safe: "#16a34a",
        danger: "#dc2626",
        warn: "#f59e0b",
        panel: "#111827",
      },
    },
  },
  plugins: [],
};
