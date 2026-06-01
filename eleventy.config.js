module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/robots.txt");

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

  // Filtro: posts relacionados (evita namespace() que não existe em Nunjucks)
  eleventyConfig.addFilter("relatedPosts", (posts, currentUrl, limit = 3) => {
    return (posts || []).filter(p => p.url !== currentUrl).slice(0, limit);
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
