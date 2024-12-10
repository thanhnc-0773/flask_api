import { useState } from "react";

export const useGalleryAction = () => {
  const [tab, setTab] = useState<string>("Gallery");

  const handleChangeTab = (tab: string) => setTab(tab);
  return { tab, handleChangeTab };
};
