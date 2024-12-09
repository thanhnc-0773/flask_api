import React from "react";
import HomeBanner from "../HomeOrganisms/HomeBanner";
import HomeSubBanner from "../HomeOrganisms/HomeSubBanner";
import BackdropSection from "../HomeOrganisms/BackdropSection";
import HomeTeam from "../HomeOrganisms/HomeTeam";

const HomeTemplate: React.FC = () => {
  return (
    <>
      <HomeBanner />

      <HomeSubBanner />

      <BackdropSection />

      <HomeTeam />
    </>
  );
};

export default HomeTemplate;
