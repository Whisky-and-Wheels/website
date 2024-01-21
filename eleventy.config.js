const path = require("path");
const Image = require("@11ty/eleventy-img");
const pluginRss = require("@11ty/eleventy-plugin-rss");

module.exports = function (eleventyConfig) {

    // group trips by year
    eleventyConfig.addFilter("groupByYear", function (trips) {
        var res = {};
        var years = [];
        // trip is a list object
        for (idx in trips) {
            var key = trips[idx].date.getFullYear();
            (res[key] || (res[key] = [])).push(trips[idx]);
            if (years.indexOf(key) == -1) { years.push(key) }

        }
        var output = { years: years, sorted_trips: res };
        return output;
    });

    // https://www.11ty.dev/docs/plugins/rss/
    eleventyConfig.addPlugin(pluginRss);

    // straight from the docs:
    // https://www.11ty.dev/docs/plugins/image/#nunjucks-liquid-javascript-(asynchronous-shortcodes)
    eleventyConfig.addShortcode("image", async function (src, alt, classes = "") {
        let metadata = await Image(src, {
            widths: [300, 600, 900, 1200, 1500],
            formats: ["avif", "jpeg"],
            outputDir: "./_site/img",
            urlPath: "/img/",
            filenameFormat: function (id, src, width, format, options) {
                const extension = path.extname(src);
                const name = path.basename(src, extension);

                return `${name}-${width}w.${format}`;
            },
        });

        // todo: loading argument, sometimes eager preferred
        let imageAttributes = {
            alt,
            sizes: "100vw",
            loading: "lazy",
            decoding: "async",
            class: classes,
        };

        // You bet we throw an error on a missing alt (alt="" works okay)
        return Image.generateHTML(metadata, imageAttributes);
    });

    // Copy jpegs
    eleventyConfig.addPassthroughCopy("img");

    // Copy maps
    eleventyConfig.addPassthroughCopy("maps");

    // Copy font
    eleventyConfig.addPassthroughCopy("font");

    // Copy css
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
