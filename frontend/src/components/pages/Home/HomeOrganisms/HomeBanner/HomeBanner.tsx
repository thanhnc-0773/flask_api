import React, { useContext } from "react";
import banner from "src/assets/images/Dragon_motor_11.jpg";
import "./HomeBanner.css";
import { HomeContext } from "../../context/HomeContext";

const HomeBanner: React.FC = () => {
  const { scrollPosition } = useContext(HomeContext);

  return (
    <div className="banner-container animate-me">
      <img src={banner} alt="banner" className="home-banner" />

      <div
        className="banner-modal"
        style={{
          transform: `translateY(${scrollPosition * 0.2}px)`,
          opacity: Math.max(1 - scrollPosition / 300, 0),
        }}
      >
        <div className="content-left-top">Escape and Explore</div>
        <p className="content-description">Embark on adventures, partake in battles, and make new encounters.</p>
      </div>

      <div
        className="vertical-text-container"
        style={{
          transform: `translateY(${scrollPosition * 0.2}px) rotate(180deg)`,
          opacity: Math.max(1 - scrollPosition / 300, 0),
        }}
      >
        <h1 className="vertical-title">NEW PLANET</h1>
        <p className="vertical-description">
          UNSATISFIED WITH THE OLD EARTH? <br />
          WHY NOT MOVE TO A NEW ONE?
        </p>
      </div>

      <div className="fade-overlay" style={{ height: `${scrollPosition}px` }} />
    </div>
  );
};

export default HomeBanner;
