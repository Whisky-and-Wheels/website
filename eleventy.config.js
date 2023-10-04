const Image = require("@11ty/eleventy-img");

module.exports = function (eleventyConfig) {
  // straight from the docs:
  // https://www.11ty.dev/docs/plugins/image/#nunjucks-liquid-javascript-(asynchronous-shortcodes)
  eleventyConfig.addShortcode("image", async function (src, alt, sizes) {
    let metadata = await Image(src, {
      widths: [300, 600],
      formats: ["webp", "jpeg"],
    });

    let imageAttributes = {
      alt,
      sizes: "100vw",
      loading: "lazy",
      decoding: "async",
    };

    // You bet we throw an error on a missing alt (alt="" works okay)
    return Image.generateHTML(metadata, imageAttributes);
  });

  // Copy `img/` to `_site/img` (relative to site dir, not input dir)
  eleventyConfig.addPassthroughCopy("img");

  // Copy font
  eleventyConfig.addPassthroughCopy("font");

  // Copy font
  eleventyConfig.addPassthroughCopy("css");

  // Include CSS in watch updates on dev
  eleventyConfig.addWatchTarget("css");

  // use excerpt delimiter
  // https://www.11ty.dev/docs/data-frontmatter-customize/#example-parse-excerpts-from-content
  eleventyConfig.setFrontMatterParsingOptions({
    excerpt: true,
    // Optional, default is "---"
    excerpt_separator: "<!-- excerpt -->",
  });

  // customize input dir
  return {
    dir: {
      input: "content",
    },
  };
};
