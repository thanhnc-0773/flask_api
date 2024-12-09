import React, { useContext } from "react";
import banner from "src/assets/images/Banner_2.jpg";
import "./HomeBanner.css";
import { HomeContext } from "../../context/HomeContext";

type Props = {
  img?: string;
  isShowHorizontalText?: boolean;
  isShowVerticalText?: boolean;
  horizontalMainText?: string | React.ReactNode;
  horizontalSubText?: string | React.ReactNode;
  verticalMainText?: string | React.ReactNode;
  verticalSubText?: string | React.ReactNode;
};

const HomeBanner: React.FC<Props> = ({
  img,
  verticalSubText,
  verticalMainText,
  horizontalSubText,
  horizontalMainText,
  isShowVerticalText,
  isShowHorizontalText,
}) => {
  const { scrollPosition } = useContext(HomeContext);

  return (
    <div className="banner-container animate-me">
      <img src={img ?? banner} alt="banner" className="home-banner" />

      {isShowHorizontalText && (
        <div
          className="banner-modal"
          style={{
            transform: `translateY(${scrollPosition * 0.2}px)`,
            opacity: Math.max(1 - scrollPosition / 300, 0),
          }}
        >
          <div className="content-left-top">{horizontalMainText}</div>
          <p className="content-description">{horizontalSubText}</p>
        </div>
      )}

      {isShowVerticalText && (
        <div
          className="vertical-text-container"
          style={{
            transform: `translateY(${scrollPosition * 0.2}px) rotate(180deg)`,
            opacity: Math.max(1 - scrollPosition / 300, 0),
          }}
        >
          <h1 className="vertical-title">{verticalMainText}</h1>
          <p className="vertical-description">{verticalSubText}</p>
        </div>
      )}

      <div className="fade-overlay" style={{ height: `${scrollPosition}px` }} />
    </div>
  );
};

export default HomeBanner;
