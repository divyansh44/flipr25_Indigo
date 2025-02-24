// import React, { useState } from "react";
// import { ChevronUp } from "lucide-react";

// const NewsCard = ({ item }) => {
//   const [isExpanded, setIsExpanded] = useState(false);

//   return (
//     <div className="bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:shadow-xl mb-6">
//       <div className="p-6">
//         <div className="flex justify-between items-start">
//           <h2 className="text-2xl font-bold text-gray-800 mb-3">
//             {item.title}
//           </h2>
//           <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
//             {item.category}
//           </span>
//         </div>

//         <p className="text-gray-600 mb-4">{item.intro}</p>

//         <div
//           className={`transition-all duration-300 overflow-hidden ${
//             isExpanded ? "max-h-[1000px]" : "max-h-0"
//           }`}
//         >
//           <div className="space-y-4">
//             <div>
//               <h3 className="font-semibold text-gray-800">Project Details</h3>
//               <p className="text-gray-600">{item.details}</p>
//             </div>
//             <div>
//               <h3 className="font-semibold text-gray-800">Impact and Reach</h3>
//               <p className="text-gray-600">{item.impact}</p>
//             </div>
//             <div>
//               <h3 className="font-semibold text-gray-800">Vision</h3>
//               <p className="text-gray-600">{item.vision}</p>
//             </div>
//           </div>
//         </div>

//         <button
//           onClick={() => setIsExpanded(!isExpanded)}
//           className="mt-4 flex items-center text-blue-600 hover:text-blue-800 transition-colors duration-200"
//         >
//           {isExpanded ? "Read less" : "Read more"}
//           <ChevronUp
//             className={`ml-1 h-4 w-4 transition-transform duration-200 ${
//               isExpanded ? "rotate-180" : ""
//             }`}
//           />
//         </button>
//       </div>
//     </div>
//   );
// };

// export default NewsCard;

import React, { useState } from "react";
import { ChevronUp } from "lucide-react";
console.log("fdsf");
const NewsCard = ({ item }) => {
  console.log("fdsf");
  const [isExpanded, setIsExpanded] = useState(false);
  console.log("item");
  console.log(item.image_urls);
  return (
    <div className="bg-black rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:shadow-xl mb-6">
      {/* Display the image */}
      {item.image_urls && (
        <img
          src={item.image_urls}
          alt={item.title}
          className="w-full h-48 object-cover rounded-t-lg"
        />
      )}

      <div className="p-6">
        <div className="flex justify-between items-start">
          {/* <h2 className="text-2xl font-bold text-gray-800 mb-3">
            {item.title}
          </h2> */}
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
            {item.category}
          </span>
        </div>

        <p className="text-gray-600 mb-4">{item.intro}</p>

        <div
          className={`transition-all duration-300 overflow-hidden ${
            isExpanded ? "max-h-[1000px]" : "max-h-0"
          }`}
        >
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-gray-800">Project Details</h3>
              <p className="text-gray-600">{item.details}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-800">Impact and Reach</h3>
              <p className="text-gray-600">{item.impact}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-800">Vision</h3>
              <p className="text-gray-600">{item.vision}</p>
            </div>
          </div>
        </div>

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="mt-4 flex items-center text-blue-600 hover:text-blue-800 transition-colors duration-200"
        >
          {isExpanded ? "Read less" : "Read more"}
          <ChevronUp
            className={`ml-1 h-4 w-4 transition-transform duration-200 ${
              isExpanded ? "rotate-180" : ""
            }`}
          />
        </button>
      </div>
    </div>
  );
};

export default NewsCard;
