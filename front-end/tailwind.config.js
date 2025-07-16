/** @type {import('tailwindcss').Config} */
module.exports = {
  
   content: [
    "./src/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {

       fontFamily: {
        michroma:['Michroma','sans-serif'],
        bitcount:['Bitcount Grid Double','sans-serif']
      },
    },
  },
  plugins: [],
}

