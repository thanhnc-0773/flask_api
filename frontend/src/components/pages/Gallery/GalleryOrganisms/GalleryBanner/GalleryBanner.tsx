import React from "react";
import banner from "src/assets/images/Dragon_motor_11.jpg";
import "./GalleryBanner.css";

const GalleryBanner: React.FC = () => {
  return (
    <div className="gallery-banner-container">
      <img src={banner} alt="banner" className="gallery-banner" />
      <div className="fade-overlay" style={{ height: `300px` }} />
    </div>
  );
};

export default GalleryBanner;
