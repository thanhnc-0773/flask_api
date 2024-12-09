import React from "react";
import { DetailArtist, DetailMember } from "./Artist.type";
import "./Artist.css";

type Props = {
  detailArtist?: DetailArtist;
  detailMember?: DetailMember;
  onSelectArtist: (id: string) => void;
  type: "artist" | "team";
};

const Artist: React.FC<Props> = ({ type, detailMember, detailArtist, onSelectArtist }) => {
  const isArtist = type === "artist";
  const id = isArtist ? detailArtist?.id : detailMember?.id;
  const avatarUrl = isArtist ? detailArtist?.avatar : detailMember?.avatar;
  const name = isArtist ? detailArtist?.name : detailMember?.name;
  const linkProfile = isArtist ? detailArtist?.x_tag : detailMember?.position;
  const description = isArtist ? detailArtist?.style : detailMember?.description;
  const link = isArtist ? detailArtist?.x_link : undefined;

  const clickXLink = (x: string) => {
    window.open(x, "_blank", "noopener,noreferrer");
  };

  return (
    <div onClick={() => id && onSelectArtist(id)} className="artist-container">
      <div className="avatar-artist-container">
        <img src={avatarUrl} alt={name} />
      </div>
      <div className="artist-detail-container">
        <div className="artist-name">{name}</div>
        <div className={`artist-link ${isArtist ? "artist" : ""}`} onClick={link ? () => clickXLink(link) : undefined}>
          {linkProfile}
        </div>
        <p className="artist-style">{description}</p>
      </div>
    </div>
  );
};

export default Artist;

export const ArtistContainer: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <div className="artist-list-container">{children}</div>;
};
