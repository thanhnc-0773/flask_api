import routesName from "src/routes/enum.routes";

export type MenuItem = {
  title: string;
  url: string;
};

export const MENU_ARRAY: MenuItem[] = [
  { title: "Home", url: routesName.ROOT },
  { title: "Gallery", url: routesName.GALLERY },
  { title: "Order", url: routesName.ROOT },
  { title: "About", url: routesName.ROOT },
];
