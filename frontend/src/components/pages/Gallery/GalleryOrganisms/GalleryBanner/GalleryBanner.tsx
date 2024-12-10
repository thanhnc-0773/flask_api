import React, { useContext } from "react";
import HomeBanner from "src/components/pages/Home/HomeOrganisms/HomeBanner";
import { GalleryContext } from "../../context";
import { TAB_BANNER_TEXT } from "../../Gallery.type";
import "./GalleryBanner.css";

const GalleryBanner: React.FC = () => {
  const { tab, scrollPosition } = useContext(GalleryContext);

  return (
    <HomeBanner
      scrollPosition={scrollPosition}
      isShowVerticalText={true}
      isShowHorizontalText={true}
      horizontalMainText={"Choose and fit"}
      horizontalSubText={"Choose the product you like and that fits with your style"}
      verticalMainText={TAB_BANNER_TEXT[tab as keyof typeof TAB_BANNER_TEXT]}
      verticalSubText={
        <>
          Not satisfied with the old product <br /> Why not search for a new one?
        </>
      }
    />
  );
};

export default GalleryBanner;
