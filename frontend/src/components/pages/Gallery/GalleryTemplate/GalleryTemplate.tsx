import React, { useContext } from "react";
import GalleryAction from "../GalleryOrganisms/GalleryAction";
import GalleryBanner from "../GalleryOrganisms/GalleryBanner";
import "./GalleryTemplate.css";
import ModalBase from "src/components/atoms/Modal";
import { GalleryContext } from "../context";
import ModalPreviewImage from "src/components/atoms/Modal/ModalPreviewImage";

const GalleryTemplate: React.FC = () => {
  const { images } = useContext(GalleryContext);

  return (
    <div className="gallery-template">
      <GalleryBanner />

      <GalleryAction />

      <ModalBase
        isShow={false}
        size="xl"
        onClose={() => {
          console.log("close");
        }}
      >
        <ModalPreviewImage images={images} initialIndex={19} />
      </ModalBase>
    </div>
  );
};

export default GalleryTemplate;
