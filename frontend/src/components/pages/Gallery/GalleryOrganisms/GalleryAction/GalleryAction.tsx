import React, { useContext } from "react";
import { Tab, Tabs } from "react-bootstrap";
import { GalleryContext } from "../../context";
import ArtistList from "../ArtistList";
import GalleryList from "../GalleryList";
import "./GalleryAction.css";

const GalleryAction: React.FC = () => {
  const { tab, loading, totalArtist, observerRef, totalGallery, handleChangeTab } = useContext(GalleryContext);
  return (
    <div className="gallery-action-container">
      <Tabs activeKey={tab} onSelect={(tab) => tab && handleChangeTab(tab)}>
        <Tab
          eventKey="Gallery"
          title={
            <>
              Fan Art <span style={{ fontSize: "15px" }}>({totalGallery})</span>
            </>
          }
        >
          <GalleryList />
        </Tab>
        <Tab
          eventKey="Artist"
          title={
            <>
              Artist <span style={{ fontSize: "15px" }}>({totalArtist})</span>
            </>
          }
        >
          <ArtistList />
        </Tab>
      </Tabs>

      {loading && <div className="loading">Loading...</div>}
      <div ref={observerRef} className="observer-trigger"></div>
    </div>
  );
};

export default GalleryAction;
