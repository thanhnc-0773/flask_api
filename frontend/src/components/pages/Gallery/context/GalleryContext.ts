import React from "react";
import { DetailArtist } from "src/components/atoms/Artist/Artist.type";
import { ImageList } from "../Gallery.type";

export interface GalleryContextProps {
  tab: string;
  images: ImageList[];
  isLoading: boolean;
  listArtist: DetailArtist[];
  observerRef: React.MutableRefObject<HTMLDivElement | null>;
  scrollPosition: number;
  onSelectArtist: (id: string) => void;
  handleChangeTab: (tab: string) => void;
}

export const GalleryContext = React.createContext<GalleryContextProps>({} as GalleryContextProps);
export const GalleryContextProvider = GalleryContext.Provider;
