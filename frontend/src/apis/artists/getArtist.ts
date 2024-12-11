import { DetailArtist } from "src/components/atoms/Artist/Artist.type";
import { endpoint } from "src/const/endpoint";
import httpRequest from "src/utilities/services/httpRequest";

export type ListArtistType = {
  current_page: number;
  datas: DetailArtist[];
  total_pages: number;
  total_records: number;
};

export type ListArtistAPIParams = {
  page: number;
};

export function getListArtist(params: ListArtistAPIParams) {
  const stringParams = Object.fromEntries(Object.entries(params).map(([key, value]) => [key, String(value)]));
  const searchParams = new URLSearchParams(stringParams).toString();

  return httpRequest.get<ListArtistType>(`${endpoint.artist}?${searchParams}`);
}
