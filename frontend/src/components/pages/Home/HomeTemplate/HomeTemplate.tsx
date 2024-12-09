import React from "react";
import HomeBanner from "../HomeOrganisms/HomeBanner";
import HomeSubBanner from "../HomeOrganisms/HomeSubBanner";
import BackdropSection from "../HomeOrganisms/BackdropSection";
import HomeTeam from "../HomeOrganisms/HomeTeam";

const HomeTemplate: React.FC = () => {
  return (
    <>
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

      <HomeSubBanner />

      <BackdropSection />

      <HomeTeam />
    </>
  );
};

export default HomeTemplate;
