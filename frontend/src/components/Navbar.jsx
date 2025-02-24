import React, { useState } from "react";
import { Newspaper, ChevronDown } from "lucide-react";

const Navbar = ({ categories, selectedCategory, onCategoryChange }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const predefinedCategories = [
    "All",
    "Sports",
    "Technology",
    "Education",
    "Crime",
    "Politics",
    "Others",
    ...categories.filter(
      (cat) =>
        ![
          "All",
          "Sports",
          "Technology",
          "Education",
          "Crime",
          "Politics",
          "Others"
        ].includes(cat)
    ),
  ];

  return (
    <nav className="sticky top-0 bg-white shadow-md z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Newspaper className="h-8 w-8 text-blue-600" />
            <span className="ml-2 text-xl font-bold text-gray-800">
              NewsHub
            </span>
          </div>

          <div className="relative">
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-200"
            >
              Explore Categories
              <ChevronDown
                className={`ml-2 h-4 w-4 transition-transform duration-200 ${
                  isDropdownOpen ? "rotate-180" : ""
                }`}
              />
            </button>

            {isDropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                {predefinedCategories.map((category, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      onCategoryChange(category);
                      setIsDropdownOpen(false);
                    }}
                    className={`block w-full text-left px-4 py-2 text-sm ${
                      selectedCategory === category
                        ? "bg-blue-50 text-blue-600"
                        : "text-gray-700 hover:bg-gray-50"
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
