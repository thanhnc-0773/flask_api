import React, { useState } from "react";
import { Carousel } from "react-bootstrap";
import { ImageList } from "src/components/pages/Gallery/Gallery.type";
import "./ModalPreviewImage.css";

type Props = { images: ImageList[]; initialIndex: number };

const ModalPreviewImage: React.FC<Props> = ({ images, initialIndex = 0 }) => {
  const [currentIndex, setCurrentIndex] = useState(initialIndex);

  const handleSelect = (selectedIndex: number) => {
    setCurrentIndex(selectedIndex);
  };

  const getDotsToShow = () => {
    const totalDots = images.length;
    const dotsToShow = 5;
    const half = Math.floor(dotsToShow / 2);

    if (totalDots <= dotsToShow) {
      return Array.from({ length: totalDots }, (_, i) => i);
    }

    if (currentIndex <= half) {
      return Array.from({ length: dotsToShow }, (_, i) => i);
    }

    if (currentIndex >= totalDots - half - 1) {
      return Array.from({ length: dotsToShow }, (_, i) => totalDots - dotsToShow + i);
    }

    return Array.from({ length: dotsToShow }, (_, i) => currentIndex - half + i);
  };

  const canGoNext = currentIndex < images.length - 1;
  const canGoPrev = currentIndex > 0;

  return (
    <div className="modal-preview-container">
      <Carousel
        activeIndex={currentIndex}
        onSelect={handleSelect}
        indicators={false}
        controls={false}
        fade={false}
        interval={null}
      >
        {images.map((image, index) => (
          <Carousel.Item key={index}>
            <img className="d-block w-100 image-preview" src={image.src} alt={image.alt || `Image ${index + 1}`} />
          </Carousel.Item>
        ))}
      </Carousel>

      <div className="carousel-controls">
        {canGoPrev && (
          <button className="carousel-btn prev-btn" onClick={() => handleSelect(currentIndex - 1)}>
            ❮
          </button>
        )}

        {canGoNext && (
          <button className="carousel-btn next-btn" onClick={() => handleSelect(currentIndex + 1)}>
            ❯
          </button>
        )}
      </div>

      <div className="carousel-index">
        <span>
          {currentIndex + 1} / {images.length}
        </span>
      </div>

      <div className="carousel-dots">
        {getDotsToShow().map((index) => (
          <span
            key={index}
            className={`dot ${currentIndex === index ? "active-dot" : ""}`}
            onClick={() => handleSelect(index)}
            style={currentIndex === index ? { animation: "scale-up 0.3s ease-in-out" } : undefined}
          ></span>
        ))}
      </div>
    </div>
  );
};

export default ModalPreviewImage;
