import { useCallback, useEffect, useRef, useState } from "react";
import { ImageList } from "../Gallery.type";

const fetchImages = (start: number, limit: number): Promise<ImageList[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const newImages = Array.from({ length: limit }, (_, index) => ({
        id: Math.floor(Math.random() * 100) + Math.random() * index,
        src: `https://picsum.photos/id/${start + index}/${Math.floor(Math.random() * 100) + 1000}/${
          Math.floor(Math.random() * 200) + 1000
        }`,
        alt: `Random Image ${start + index}`,
      }));
      resolve(newImages);
    }, 1000);
  });
};

type Props = { tab: string };

export const useGallery = ({ tab }: Props) => {
  const [images, setImages] = useState<ImageList[]>([]);
  const [page, setPage] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const observerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const loadImages = async () => {
      setIsLoading(true);
      const newImages = await fetchImages((page - 1) * 12, 12);
      setImages((prev) => [...prev, ...newImages]);
      setIsLoading(false);
    };

    tab === "Gallery" && loadImages();
  }, [page, tab]);

  const handleObserver: IntersectionObserverCallback = useCallback(
    (entries) => {
      const [target] = entries;
      if (target.isIntersecting && !isLoading) {
        setPage((prev) => prev + 1);
      }
    },
    [isLoading]
  );

  useEffect(() => {
    const observer = new IntersectionObserver(handleObserver, {
      root: null,
      rootMargin: "200px",
      threshold: 0.1,
    });

    if (observerRef.current) observer.observe(observerRef.current);

    return () => {
      if (observerRef.current) observer.unobserve(observerRef.current);
    };
  }, [handleObserver]);

  return { page, images, isLoading, observerRef };
};
