import React, { useEffect, useState } from "react";
import "./Menubar.css";
import { MENU_ARRAY } from "./Menubar.type";
import { useNavigate } from "react-router-dom";
import logoWhite from "src/assets/images/HTC_logo_White_1.png";

const Menubar: React.FC = () => {
  const [scrollProgress, setScrollProgress] = useState(0);
  const navigate = useNavigate();

  const handleScroll = () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const progress = (scrollTop / scrollHeight) * 100;
    setScrollProgress(progress);
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleNavigate = (url: string) => {
    navigate(url);
  };

  return (
    <div className="menubar">
      <img src={logoWhite} alt="logo" className="logo-white" width={50} />

      <nav className="nav">
        <ul className="nav-list">
          {MENU_ARRAY.map((m) => {
            return (
              <li key={m.title} className="nav-item" onClick={() => handleNavigate(m.url)}>
                {m.title}
              </li>
            );
          })}
        </ul>
      </nav>
      <div
        className="progress"
        style={{
          width: `${scrollProgress}%`,
        }}
      ></div>

      <div className="icon-menu">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          className="bi bi-list"
          viewBox="0 0 16 16"
        >
          <path d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5" />
        </svg>
      </div>
    </div>
  );
};

export default Menubar;
