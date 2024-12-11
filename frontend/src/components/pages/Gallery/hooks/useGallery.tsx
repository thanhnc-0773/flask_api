import { useCallback, useEffect, useRef, useState } from "react";
import { getListGallery } from "src/apis/galleries/getGallery";
import { useAppDispatch, useAppSelector } from "src/app/appHooks";
import { setState } from "src/slices/appSlice";
import { ImageList } from "../Gallery.type";

type Props = {
  tab: string;
  page: number;
  loading: boolean;
  totalPage: number;
  handleChangePage: React.Dispatch<React.SetStateAction<number>>;
  handleChangeTotal: React.Dispatch<React.SetStateAction<number>>;
};

export const useGallery = ({ tab, page, loading, totalPage, handleChangePage, handleChangeTotal }: Props) => {
  const dispatch = useAppDispatch();

  const [images, setImages] = useState<ImageList[]>([]);
  const [totalGallery, setTotalGallery] = useState<number>(0);

  const observerRef = useRef<HTMLDivElement | null>(null);

  const getListGalleryFnc = (currPage: number) => {
    dispatch(setState({ loading: true }));
    getListGallery({ page: currPage })
      .then((res) => {
        setImages(res.datas);
        handleChangeTotal(res.total_pages);
        setTotalGallery(res.total_records ?? 0);
      })
      .finally(() => dispatch(setState({ loading: false })));
  };

  useEffect(() => {
    if (tab === "Gallery" && page <= totalPage) getListGalleryFnc(page);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, tab]);

  const handleObserver: IntersectionObserverCallback = useCallback(
    (entries) => {
      const [target] = entries;
      if (target.isIntersecting && !loading && page < totalPage) {
        handleChangePage((prev) => prev + 1);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [loading]
  );

  useEffect(() => {
    const observer = new IntersectionObserver(handleObserver, {
      root: null,
      rootMargin: "200px",
      threshold: 0.1,
    });

    if (observerRef.current) observer.observe(observerRef.current);

    return () => {
      // eslint-disable-next-line react-hooks/exhaustive-deps
      if (observerRef.current) observer.unobserve(observerRef.current);
    };
  }, [handleObserver]);

  return { page, images, observerRef, totalGallery };
};
