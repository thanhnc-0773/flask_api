export interface HomeKOLs {
  id: number;
  name: string;
  link_x: string;
  avatar: string;
}

export const dumpKOLs: HomeKOLs[][] = [
  [
    { id: 1, avatar: "https://picsum.photos/200", name: "Zero One", link_x: "https://example.com/1" },
    { id: 2, avatar: "https://picsum.photos/200", name: "Zero Two", link_x: "https://example.com/2" },
    { id: 3, avatar: "https://picsum.photos/200", name: "Zero Three", link_x: "https://example.com/3" },
  ],
  [
    { id: 4, avatar: "https://picsum.photos/200", name: "Zero Four", link_x: "https://example.com/4" },
    { id: 5, avatar: "https://picsum.photos/200", name: "Zero Five", link_x: "https://example.com/5" },
    { id: 6, avatar: "https://picsum.photos/200", name: "Zero Six", link_x: "https://example.com/6" },
  ],
  [
    { id: 7, avatar: "https://picsum.photos/200", name: "Zero Seven", link_x: "https://example.com/7" },
    { id: 8, avatar: "https://picsum.photos/200", name: "Zero Eight", link_x: "https://example.com/8" },
    { id: 9, avatar: "https://picsum.photos/200", name: "Zero Nine", link_x: "https://example.com/9" },
  ],
];
