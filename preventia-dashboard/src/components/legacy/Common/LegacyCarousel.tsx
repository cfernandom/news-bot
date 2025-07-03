import React, { useState, useEffect, useCallback } from 'react';

interface CarouselSlide {
  id: number;
  icon: string;
  title: string;
  content: string;
}

interface LegacyCarouselProps {
  slides: CarouselSlide[];
  autoAdvance?: boolean;
  autoAdvanceDelay?: number;
}

const LegacyCarousel: React.FC<LegacyCarouselProps> = ({
  slides,
  autoAdvance = true,
  autoAdvanceDelay = 5000
}) => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const nextSlide = useCallback(() => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  }, [slides.length]);

  const prevSlide = useCallback(() => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  }, [slides.length]);

  const goToSlide = useCallback((index: number) => {
    setCurrentSlide(index);
  }, []);

  // Auto-advance carousel
  useEffect(() => {
    if (!autoAdvance) return;

    const interval = setInterval(nextSlide, autoAdvanceDelay);
    return () => clearInterval(interval);
  }, [autoAdvance, autoAdvanceDelay, nextSlide]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowLeft') {
        prevSlide();
      } else if (event.key === 'ArrowRight') {
        nextSlide();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [nextSlide, prevSlide]);

  if (slides.length === 0) return null;

  return (
    <div className="legacy-carousel-container">
      <div className="legacy-carousel-wrapper">
        <div
          className="legacy-carousel"
          style={{ transform: `translateX(-${currentSlide * 100}%)` }}
        >
          {slides.map((slide) => (
            <div key={slide.id} className="legacy-carousel-slide">
              <div className="legacy-carousel-content">
                <i className={`fas ${slide.icon} legacy-carousel-icon`}></i>
                <h3 className="legacy-carousel-title">{slide.title}</h3>
                <p className="legacy-carousel-text">{slide.content}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <button
        className="legacy-carousel-nav prev"
        onClick={prevSlide}
        aria-label="Previous slide"
      >
        ❮
      </button>

      <button
        className="legacy-carousel-nav next"
        onClick={nextSlide}
        aria-label="Next slide"
      >
        ❯
      </button>

      <div className="legacy-carousel-indicators">
        {slides.map((_, index) => (
          <button
            key={index}
            className={`legacy-carousel-indicator ${index === currentSlide ? 'active' : ''}`}
            onClick={() => goToSlide(index)}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </div>
  );
};

export default LegacyCarousel;
