# Wheels and Whisky

<img src="https://raw.githubusercontent.com/whisky-and-wheels/website/main/img/favicon/android-chrome-512x512.png" alt="Whisky and Wheels logo" style="float: right; margin-right: 50px" align="right" width=250px/>

## Install

```bash
npm install
npm start
```

## 11ty platform

- Allow markdown content
- Flexible configuration
- Nunjucks templating
- No client-side JS by default

## Font

Variable font served locally: [Fraunces](https://fonts.google.com/specimen/Fraunces/tester), sourced from Google Fonts

## Favicon

Generated by <https://favicon.io/favicon-converter/>

## Architecture

### Cascade Layers

I **love** that you can append to a layer from anywhere. And I'm enjoying being able to close layer blocks in my editor to focus on the styles I'm working on without distraction.

There are a lot of ways to organize this. I changed my approach multiple times.

Definitely makes the most sense for reset/default styles. Would be useful for overriding third-party styles too, although I don't intend to use those in the case. I went back and forth between nesting reset layer inside default layer. It's a little easier to read flat layers in the dev tools but I'm keeping nested for now, as the reset doesn't make sense without defaults in my mind.

I wanted to use component with nested block/modifier layers, but the modifier layer didn't feel specific enough, so I split it to variant/state. Unlayered styles take precedence over layered ones so that means I need to layer the base component styles too (~I've tentatively named this component.block, but I don't love it, feels too easy to forget this layer is required~ update: I decided to un-nest here).

I also had `layout` instead of `template` at first, but I confused myself with what belonged in that layer. Template was easier to remember as more of an atomic styling approach. Context-agnostic styles go in component layers; context-specific styles go in template layers.

I like utility as final layer with often-used defaults and custom property overrides. It's nice to see at a glance in the HTML what containers are using what layout context. I might expand this to `u-text-*` helpers too, but I'm not sure how much further I'd go. Maybe `u-block-spacing-*` and `u-inline-spacing-*`? Worth a try.

I'm not totally convinced I need the theme layer. Setting custom properties on the page or element would do the job too. But I like the reusability and declarative nature of data attribute theming.

I'm adding an "exceptions" escape hatch layer. Curious to see if I reach for this much, if at all. If it's used a lot, it would be indicative of bigger structural problems.

I may move to avoiding nesting within component layer, so the general structure would be:
`@layer default, component, variant, state, template, utility, theme, exception`

### Web Components

The labels seem to be a good use case for this. Moving everything around with grid feels bad.

## TODO

### Configuration

- add sizes to image shortcode
- adjust returned HTML to allow figure & figcaption

### Templating

- set up meta content that accepts page specific variables
- set up HTML framework skeleton (head, header, main, footer)
- partial for trip map/stats

### Styling

- MVP for browsers that don't support cascade layers (that works as a proxy for a lot of other modern CSS support), need to watch out for nesting support too (it's implemented with older spec in most browsers)
- Container queries for label styling and trip stats
- Trip layout:
  - Sticky stat sidebars
  - Scrollbased animation for map to move to sidebar and highlight appropriate path for day
- clean up use of magic numbers in parallax styles
