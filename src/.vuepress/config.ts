import { defineUserConfig } from "vuepress";

import theme from "./theme.js";

export default defineUserConfig({
  base: "/TyrionBlogs/",

  locales: {
    "/": {
      lang: "zh-CN",
      title: "Tyrio’s Blogs",
      description: "Share my knowledge and thoughts",
    }
  },

  theme,

  // Enable it with pwa
  // shouldPrefetch: false,
});
