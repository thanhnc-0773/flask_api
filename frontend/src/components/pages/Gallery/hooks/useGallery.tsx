import { useCallback, useEffect, useRef, useState } from "react";
import { getListGallery } from "src/apis/galleries/getGallery";
import { useAppDispatch } from "src/app/appHooks";
import { setState } from "src/slices/appSlice";
import { ImageList } from "../Gallery.type";

type Props = {
  tab: string;
  page: number;
  loading: boolean;
  totalPage: number;
  isFirstMount: React.MutableRefObject<{
    gallery: boolean;
    artist: boolean;
  }>;
  handleChangePage: React.Dispatch<React.SetStateAction<number>>;
  handleChangeTotal: React.Dispatch<React.SetStateAction<number>>;
};

export const useGallery = ({
  tab,
  page,
  loading,
  totalPage,
  isFirstMount,
  handleChangePage,
  handleChangeTotal,
}: Props) => {
  const dispatch = useAppDispatch();

  const [images, setImages] = useState<ImageList[]>([]);
  const [totalGallery, setTotalGallery] = useState<number>(0);

  const observerRef = useRef<HTMLDivElement | null>(null);

  const getListGalleryFnc = useCallback(
    (currPage: number) => {
      dispatch(setState({ loading: true }));
      getListGallery({ page: currPage })
        .then((res) => {
          setImages((prev) => {
            return currPage === 1 ? res.datas : [...prev, ...res.datas];
          });
          handleChangeTotal(res.total_pages);
          setTotalGallery(res.total_records ?? 0);
        })
        .finally(() => dispatch(setState({ loading: false })));
    },
    [dispatch, handleChangeTotal]
  );

  useEffect(() => {
    if ((tab === "Gallery" && page <= totalPage) || isFirstMount.current.gallery) {
      getListGalleryFnc(page);

      if (isFirstMount.current.gallery) {
        isFirstMount.current = { ...isFirstMount.current, gallery: false };
      }
    }
  }, [getListGalleryFnc, isFirstMount, page, tab, totalPage]);

  const handleObserver: IntersectionObserverCallback = useCallback(
    (entries) => {
      const [target] = entries;

      if (target.isIntersecting && !loading && page < totalPage) {
        handleChangePage((prev) => prev + 1);
      }
    },
    [handleChangePage, loading, page, totalPage]
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
