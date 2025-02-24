import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import NewsList from "./components/NewsList";
import Footer from "./components/Footer";

const App = () => {
  const [news, setNews] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  // Helper function to extract title and paragraphs
  const parseContent = (content) => {
    const lines = content.split("\n").filter((line) => line.trim());
    const title = lines[0].replace("Title: ", "");
    const paragraphs = lines.slice(1).reduce((acc, line) => {
      // Skip section headers (lines ending with ':')
      if (!line.endsWith(":")) {
        acc.push(line);
      }
      return acc;
    }, []);

    return { title, paragraphs };
  };

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true);
        const response = await fetch("http://127.0.0.1:5000/news");
        if (!response.ok) throw new Error("Failed to fetch news");
        const data = await response.json();
        console.log(data);
        const formattedNews = data.news.map((item) => {
          const { title, paragraphs } = parseContent(item.content);
          console.log("dfadsdfafdsf");
          console.log(item.category);
          if (item.category == "Sports") {
            console.log("aa");
            console.log(item.image_urls);
          }
          console.log(item.image_urls);
          return {
            category: item.category || "General",
            title,
            paragraphs,
            image_urls: item.image_urls,
          };
        });
        // Collect unique categories
        const uniqueCategories = [
          "All",
          ...new Set(formattedNews.map((item) => item.category)),
        ];

        setNews(formattedNews);
        setCategories(uniqueCategories);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
    const interval = setInterval(fetchNews, 500000);
    return () => clearInterval(interval);
  }, []);

  const filteredNews =
    selectedCategory === "All"
      ? news
      : news.filter((item) => item.category === selectedCategory);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar
        categories={categories}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
      />

      <main className="container mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            <h1 className="text-3xl font-bold text-gray-800 mb-8">
              {selectedCategory === "All"
                ? "Latest News"
                : `${selectedCategory} News`}
            </h1>
             
            {/* <div>
              <img
                src="https://i.ibb.co/TBgxkkBR/0-jpg.jpg"
                alt="{item.title}"
                className="w-full h-48 object-cover rounded-t-lg"
              />
            </div> */}
            <div className="grid gap-6">
              {filteredNews.map((item, index) => (
                <article
                  key={index}
                  className="bg-white rounded-lg shadow-md p-6"
                >
                  {item.image_urls && (
                    <img
                      src={item.image_urls}
                      alt={item.title}
                      className="w-full h-48 object-cover rounded-t-lg"
                    />
                  )}
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">
                    {item.title}
                  </h2>
                  <div className="space-y-4">
                    {item.paragraphs.map((paragraph, pIndex) => (
                      <p key={pIndex} className="text-gray-600 leading-relaxed">
                        {paragraph}
                      </p>
                    ))}
                  </div>
                  <div className="mt-4 inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    {item.category}
                  </div>
                </article>
              ))}
            </div>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default App;
