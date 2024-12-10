import { DetailArtist } from "src/components/atoms/Artist/Artist.type";
import { endpoint } from "src/const/endpoint";
import httpRequest from "src/utilities/services/httpRequest";

export function getListArtist() {
  return httpRequest.get<DetailArtist[]>(endpoint.artist);
}
