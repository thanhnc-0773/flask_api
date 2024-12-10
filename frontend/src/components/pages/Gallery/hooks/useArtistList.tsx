import { useEffect, useState } from "react";
import { getListArtist } from "src/apis/artists/getArtist";
import { DetailArtist } from "src/components/atoms/Artist/Artist.type";

export const useArtistList = () => {
  const [listArtist, setListArtist] = useState<DetailArtist[]>([]);

  const onSelectArtist = (id: string) => {
    console.log("id", id);
  };

  const getListArtistFnc = () => {
    getListArtist().then((res) => {
      setListArtist(res);
    });
  };

  useEffect(() => {
    getListArtistFnc();
  }, []);

  return { listArtist, onSelectArtist };
};
