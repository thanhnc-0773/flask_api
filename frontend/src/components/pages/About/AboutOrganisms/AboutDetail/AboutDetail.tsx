import React from "react";
import banner from "src/assets/images/img-1.webp";

const AboutDetail: React.FC = () => {
  return (
    <div className="about-detail-container">
      <div className="about-detail-top">
        <div className="about-detail-top-description">
          <div className="des-top">WHAT IS L3E7 WORLDS?</div>
          <div className="des-bottom">
            The L3E7 Worlds NFT collection, limited to only 600 NFTs, acts as an early access pass. It grants holders a
            range of exclusive benefits, symbolizing their premier stake within the ecosystem.
          </div>
        </div>

        <div className="about-detail-top-action">
          <a href="/gallery" className="detail-top-button">
            Browse Collection
          </a>
        </div>
      </div>

      <div className="about-detail-bottom">
        <div className="about-detail-bottom-left">
          <div className="bottom-left-text">
            <div className="des-top" style={{ lineHeight: "unset" }}>
              DESIGN CONCEPT
            </div>
            <div className="des-bottom" style={{ margin: 0 }}>
              Every NFT within this collection is procedurally crafted using 18 distinct animated assets as its
              foundation
            </div>
          </div>

          <div className="bottom-left-text">
            <div className="des-top">UTILITY</div>
            <div className="des-bottom" style={{ margin: 0 }}>
              Benefits
            </div>

            <ul className="des-bottom-list">
              <li>
                <span>Reserved spot in the private presale of L3E7 upcoming collections</span>
              </li>
              <li>
                <span>Gain Sharing from the Ecosystem</span>
              </li>
              <li>
                <span>In-Game Reward Booster</span>
              </li>
              <li>
                <span>Priority Access to the Game Test</span>
              </li>
              <li>
                <span>IRL Events</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="about-detail-bottom-right" style={{ padding: 0 }}>
          <img src={banner} alt="banner" />
        </div>
      </div>
    </div>
  );
};

export default AboutDetail;
