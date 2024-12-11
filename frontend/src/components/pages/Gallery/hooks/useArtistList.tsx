import { useEffect, useState } from "react";
import { getListArtist } from "src/apis/artists/getArtist";
import { useAppDispatch } from "src/app/appHooks";
import { DetailArtist } from "src/components/atoms/Artist/Artist.type";
import { setState } from "src/slices/appSlice";

type Props = {
  tab: string;
  page: number;
  totalPage: number;
  handleChangePage: React.Dispatch<React.SetStateAction<number>>;
  handleChangeTotal: React.Dispatch<React.SetStateAction<number>>;
};

export const useArtistList = ({ tab, page, totalPage, handleChangeTotal }: Props) => {
  const dispatch = useAppDispatch();

  const [listArtist, setListArtist] = useState<DetailArtist[]>([]);
  const [totalArtist, setTotalArtist] = useState<number>(0);

  const onSelectArtist = (id: string) => {
    console.log("id", id);
  };

  const getListArtistFnc = (currPage: number) => {
    dispatch(setState({ loading: true }));
    getListArtist({ page: currPage })
      .then((res) => {
        setListArtist(res.datas);
        handleChangeTotal(res.total_pages);
        setTotalArtist(res.total_records ?? 0);
      })
      .finally(() => dispatch(setState({ loading: false })));
  };

  useEffect(() => {
    if (tab === "Artist" && page <= totalPage) {
      getListArtistFnc(page);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, tab]);

  return { listArtist, totalArtist, onSelectArtist };
};
