module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/robots.txt");
  // Assets de demos de prospecção (/demo/<slug>/assets/)
  eleventyConfig.addPassthroughCopy("src/demo/**/assets/**");

  eleventyConfig.addGlobalData("build", () => ({
    ts: Date.now(),
    year: new Date().getFullYear(),
  }));

  // Filtro: data em PT-BR (ex: "12 de junho de 2026")
  eleventyConfig.addFilter("dateFormat", (date) =>
    new Date(date).toLocaleDateString("pt-BR", {
      year: "numeric", month: "long", day: "numeric",
    })
  );

  // Filtro: ISO date para sitemap/schema
  eleventyConfig.addFilter("dateIso", (date) =>
    new Date(date).toISOString().split("T")[0]
  );

  // Filtro: tempo estimado de leitura
  eleventyConfig.addFilter("readingTime", (content) => {
    const text = String(content || "").replace(/<[^>]*>/g, "");
    const words = text.split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.ceil(words / 200));
  });

  // Filtro: posts relacionados — mesmo cluster primeiro, depois os mais recentes
  eleventyConfig.addFilter("relatedPosts", (posts, currentUrl, cluster, limit = 3) => {
    const others = (posts || []).filter(p => p.url !== currentUrl);
    const same   = cluster ? others.filter(p => p.data.cluster === cluster) : [];
    const rest   = others.filter(p => !same.includes(p));
    return same.concat(rest).slice(0, limit);
  });

  // Coleção: posts com data <= hoje (agendamento via build diário)
  eleventyConfig.addCollection("publishedPosts", function (collectionApi) {
    const now = new Date();
    return collectionApi
      .getFilteredByTag("posts")
      .filter((post) => post.date <= now)
      .sort((a, b) => b.date - a.date);
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
