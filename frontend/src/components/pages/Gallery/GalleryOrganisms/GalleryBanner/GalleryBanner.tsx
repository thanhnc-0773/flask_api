import React, { useContext } from "react";
import homeBanner from "src/assets/images/Banner_1.jpg";
import HomeBanner from "src/components/pages/Home/HomeOrganisms/HomeBanner";
import { GalleryContext } from "../../context";
import { TAB_BANNER_SUB_TEXT, TAB_BANNER_TEXT } from "../../Gallery.type";
import "./GalleryBanner.css";

const GalleryBanner: React.FC = () => {
  const { tab, scrollPosition } = useContext(GalleryContext);

  return (
    <HomeBanner
      img={homeBanner}
      scrollPosition={scrollPosition}
      isShowVerticalText={true}
      isShowHorizontalText={true}
      horizontalMainText={"Choose and fit"}
      horizontalSubText={"Choose the product you like and that fits with your style."}
      verticalMainText={TAB_BANNER_TEXT[tab as keyof typeof TAB_BANNER_TEXT]}
      verticalSubText={TAB_BANNER_SUB_TEXT[tab as keyof typeof TAB_BANNER_SUB_TEXT]}
    />
  );
};

export default GalleryBanner;
