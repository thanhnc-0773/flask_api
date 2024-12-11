import React, { useContext } from "react";
import { GalleryContext } from "../../context";
import "./GalleryList.css";

const GalleryList: React.FC = () => {
  const { images, onSelectGallery } = useContext(GalleryContext);

  return (
    <div className="gallery-container">
      <div className="gallery-flex">
        {images.map((image) => (
          <div key={image.id} className="gallery-item" onClick={() => onSelectGallery(image.id.toString())}>
            <img src={image.picture} alt={image.alt} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default GalleryList;
