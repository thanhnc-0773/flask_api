import { mockListArtist } from "../../Home/HomeOrganisms/HomeTeam/HomeTeam.type";

export const useArtistList = () => {
  const onSelectArtist = (id: string) => {
    console.log("id", id);
  };

  return { listArtist: mockListArtist, onSelectArtist };
};
