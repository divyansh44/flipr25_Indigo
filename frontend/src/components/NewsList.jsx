import React from "react";
import NewsCard from "./NewCard";

const NewsList = ({ news }) => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid gap-6">
        {news.map((item, index) => (
          <NewsCard key={index} item={item} />
        ))}
      </div>
    </div>
  );
};
export default NewsList;
