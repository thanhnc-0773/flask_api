import React, { useContext } from "react";
import HomeBanner from "../HomeOrganisms/HomeBanner";
import HomeSubBanner from "../HomeOrganisms/HomeSubBanner";
import BackdropSection from "../HomeOrganisms/BackdropSection";
import HomeTeam from "../HomeOrganisms/HomeTeam";
import { HomeContext } from "../context";
import homeBanner from "src/assets/images/Banner_1.jpg";

const HomeTemplate: React.FC = () => {
  const { scrollPosition } = useContext(HomeContext);
  return (
    <>
      <HomeBanner
        img={homeBanner}
        scrollPosition={scrollPosition}
        isShowVerticalText={true}
        isShowHorizontalText={true}
        horizontalMainText={"Choose and fit"}
        horizontalSubText={"Choose the product you like and that fits with your style."}
        verticalMainText={"Welcome to HTC studio"}
        verticalSubText={
          <>
            Not satisfied with the old product? <br /> Why not search for a new one?
          </>
        }
      />

      <div className="home-content-container">
        <HomeSubBanner />

        <BackdropSection />

        <HomeTeam />
      </div>
    </>
  );
};

export default HomeTemplate;
