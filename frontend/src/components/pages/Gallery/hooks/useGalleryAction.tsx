import { useState } from "react";

export const useGalleryAction = () => {
  const [tab, setTab] = useState<string>("Gallery");
  const [page, setPage] = useState<number>(1);
  const [totalPage, setTotalPage] = useState<number>(1);

  const handleChangeTab = (tab: string) => {
    setTab(tab);
    setPage(1);
    setTotalPage(1);
  };
  return { tab, page, totalPage, handleChangeTab, handleChangePage: setPage, handleChangeTotal: setTotalPage };
};
