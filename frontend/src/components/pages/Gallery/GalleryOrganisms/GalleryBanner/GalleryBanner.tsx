import React from "react";
import HomeBanner from "src/components/pages/Home/HomeOrganisms/HomeBanner";
import "./GalleryBanner.css";

const GalleryBanner: React.FC = () => {
  return (
    <HomeBanner
      isShowVerticalText={true}
      isShowHorizontalText={true}
      horizontalMainText={"Choose and fit"}
      horizontalSubText={"Choose the product you like and that fits with your style"}
      verticalMainText={"Welcome to HTC studio"}
      verticalSubText={
        <>
          Not satisfied with the old product <br /> Why not search for a new one?
        </>
      }
    />
  );
};

export default GalleryBanner;
