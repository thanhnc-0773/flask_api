import MainLayout from "src/components/layouts/MainLayout";
import AboutPage from "src/components/pages/About";
import GalleryPage from "src/components/pages/Gallery";
import HomePage from "src/components/pages/Home";
import routesName from "./enum.routes";
import { IRouterData } from "./type.routes";

export const routesData: IRouterData[] = [
  {
    path: routesName.ROOT,
    layout: MainLayout,
    component: () => <HomePage />,
  },
  {
    path: routesName.GALLERY,
    layout: MainLayout,
    component: () => <GalleryPage />,
  },
  {
    path: routesName.ABOUT,
    layout: MainLayout,
    component: () => <AboutPage />,
  },
];
