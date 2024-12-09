import React from "react";
import GalleryTemplate from "./GalleryTemplate";
import { GalleryContextProvider } from "./context";
import { useArtistList } from "./hooks/useArtistList";
import { useGallery } from "./hooks/useGallery";
import { useGalleryAction } from "./hooks/useGalleryAction";

const GalleryPage: React.FC = () => {
  const { tab, handleChangeTab } = useGalleryAction();
  const { listArtist, onSelectArtist } = useArtistList();
  const { images, isLoading, observerRef } = useGallery({ tab });

  return (
    <GalleryContextProvider
      value={{ tab: tab, images, isLoading, listArtist, observerRef, onSelectArtist, handleChangeTab }}
    >
      <GalleryTemplate />
    </GalleryContextProvider>
  );
};

export default GalleryPage;
