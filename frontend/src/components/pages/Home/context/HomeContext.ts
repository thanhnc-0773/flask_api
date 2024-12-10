import React from "react";

export interface HomeContextProps {
  scrollPosition: number;
}

export const HomeContext = React.createContext<HomeContextProps>({} as HomeContextProps);
export const HomeContextProvider = HomeContext.Provider;
