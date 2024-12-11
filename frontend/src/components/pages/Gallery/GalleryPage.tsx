import React from "react";
import { useHandleScroll } from "../Home/hooks/useHandleScroll";
import GalleryTemplate from "./GalleryTemplate";
import { GalleryContextProvider } from "./context";
import { useArtistList } from "./hooks/useArtistList";
import { useGallery } from "./hooks/useGallery";
import { useGalleryAction } from "./hooks/useGalleryAction";
import { useAppSelector } from "src/app/appHooks";

const GalleryPage: React.FC = () => {
  const { loading } = useAppSelector((state) => state.app);

  const { scrollPosition } = useHandleScroll();
  const { tab, page, totalPage, handleChangeTab, handleChangePage, handleChangeTotal } = useGalleryAction();
  const { listArtist, totalArtist, onSelectArtist } = useArtistList({
    tab,
    page,
    totalPage,
    handleChangePage,
    handleChangeTotal,
  });
  const { images, totalGallery, observerRef } = useGallery({
    tab,
    page,
    loading,
    totalPage,
    handleChangePage,
    handleChangeTotal,
  });

  return (
    <GalleryContextProvider
      value={{
        tab: tab,
        images,
        loading,
        listArtist,
        observerRef,
        totalArtist,
        totalGallery,
        scrollPosition,
        onSelectArtist,
        handleChangeTab,
      }}
    >
      <GalleryTemplate />
    </GalleryContextProvider>
  );
};

export default GalleryPage;
