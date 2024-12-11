import { DetailArtist } from "src/components/atoms/Artist/Artist.type";

export type ImageList = {
  id: number;
  picture: string;
  alt: string;
  artist_id: number;
  created_at: string;
  show_on_top: boolean;
  updated_at: string;
};

export const TAB_BANNER_TEXT = {
  Gallery: "Fan art",
  Artist: "Artist",
};

export type ModalPreviewState = {
  isShow: boolean;
  imageList: ImageList[];
  detailArtist: DetailArtist;
};
