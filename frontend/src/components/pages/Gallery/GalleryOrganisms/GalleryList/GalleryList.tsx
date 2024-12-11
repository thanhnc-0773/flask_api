import React, { useContext } from "react";
import { GalleryContext } from "../../context";
import "./GalleryList.css";

const GalleryList: React.FC = () => {
  const { images, loading, observerRef } = useContext(GalleryContext);

  return (
    <div className="gallery-container">
      <div className="gallery-flex">
        {images.map((image) => (
          <div key={image.id} className="gallery-item">
            <img src={image.picture} alt={image.alt} />
          </div>
        ))}
      </div>
      {loading && <div className="loading">Loading...</div>}
      <div ref={observerRef} className="observer-trigger"></div>
    </div>
  );
};

export default GalleryList;
