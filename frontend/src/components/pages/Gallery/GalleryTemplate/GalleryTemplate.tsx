import React, { useContext } from "react";
import ModalBase from "src/components/atoms/Modal";
import ModalPreviewImage from "src/components/atoms/Modal/ModalPreviewImage";
import { GalleryContext } from "../context";
import GalleryAction from "../GalleryOrganisms/GalleryAction";
import GalleryBanner from "../GalleryOrganisms/GalleryBanner";
import "./GalleryTemplate.css";

const GalleryTemplate: React.FC = () => {
  const { modalPreview, selectedIndex, onCloseModal } = useContext(GalleryContext);

  const renderTitle = () => {
    const onClickArtist = () => window.open(modalPreview.detailArtist.link_x, "_blank", "noopener,noreferrer");

    return (
      <div className="artist-preview-container" onClick={() => onClickArtist()}>
        <img src={modalPreview.detailArtist.avatar} alt={modalPreview.detailArtist.name} />
        <div className="artist-preview-name">{modalPreview.detailArtist.name}</div>
      </div>
    );
  };

  return (
    <div className="gallery-template">
      <GalleryBanner />

      <GalleryAction />

      <ModalBase
        isShow={modalPreview.isShow}
        size="xl"
        onClose={() => onCloseModal()}
        onBackdropClick={() => onCloseModal()}
        titleModal={renderTitle()}
      >
        <ModalPreviewImage images={modalPreview.imageList} initialIndex={selectedIndex} />
      </ModalBase>
    </div>
  );
};

export default GalleryTemplate;
