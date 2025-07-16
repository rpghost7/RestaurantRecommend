import { motion } from "framer-motion";
import { useEffect, useState } from "react";
const API_URL = process.env.REACT_APP_API_URL;
const words = [
  "Beverages",
  "Desserts",
  "Chinese",
  "Biryani",
  "Fast Food",
  "Rolls",
  "Pizza",
];

function App() {
  const [index, setIndex] = useState(0);
  const [input, setInput] = useState("");
  const [results, setResults] = useState([]); // <-- Store backend response

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % words.length);
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  const handleKeyDown = async (e) => {
    if (e.key === "Enter") {
      e.preventDefault();

      const parts = input.trim().split(" ");
      if (parts.length < 2) {
        console.error("Please enter both cuisine and city.");
        return;
      }

      const user_cuisine = parts[0];
      const user_city = parts.slice(1).join(" ");

      const body = {
        place_cuisine: user_cuisine,
        place_city: user_city,
        rating: 4.0,
        price: 300,
      };

      try {
        const res = await fetch(`${API_URL}/recommend`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        });

        const data = await res.json();
        console.log("💡 Backend results:", data);

        setResults(data.results || []);
        setInput(""); // clear input box
      } catch (err) {
        console.error("Error calling backend:", err);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center px-4">
      <h1 className="text-4xl sm:text-5xl md:text-6xl font-michroma text-gray-100 mb-8 text-center">
        What would you like to eat today?
      </h1>

      <motion.div
        key={index}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.6 }}
        className="text-5xl text-teal-500 font-bitcount pb-8"
      >
        {words[index]}
      </motion.div>

      <input
        type="text"
        placeholder="Type your craving..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        className="w-full max-w-lg px-4 py-3 mb-6 rounded-xl bg-gray-800 text-teal-400 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-pink-500 transition duration-300"
      />
      {results.length > 0 && (
        <div className="mt-8 space-y-4">
          <h2 className="text-3xl sm:text-4xl font-bold text-teal-400 mb-6">
            Top Recommendations Just for You:
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-6">
            {results.map((item, idx) => (
              <div
                key={idx}
                className="bg-gray-800 border border-teal-500 rounded-xl p-5 shadow-lg hover:scale-105 transition-transform duration-300"
              >
                <h3 className="text-xl font-semibold text-white mb-2">
                  {idx + 1}. {item.Item_Name}
                </h3>
                <p className="text-gray-300 mb-1">
                  at{" "}
                  <span className="text-teal-400">{item.Restaurant_Name}</span>
                </p>
                <p className="text-gray-400 mb-1">📍 {item.Place_Name}</p>
                <p className="text-yellow-400">
                  ⭐ {item.Average_Rating} | 💰 ₹{item.Prices}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
