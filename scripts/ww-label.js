class Label extends HTMLElement {
  constructor() {
    super();

    // create shadow root
    this.shadow = this.attachShadow({ mode: "open" });

    // add attributes
    this.href = this.getAttribute("href");
    this.inspiration = this.getAttribute("inspiration");
    this.title = this.getAttribute("title");
    this.subtitle = this.getAttribute("subtitle");
    this.days = this.getAttribute("days");
    this.kilometres = this.getAttribute("kilometres");
    this.start = this.getAttribute("start");
    this.end = this.getAttribute("end");
  }

  connectedCallback() {
    console.log("connected");
    this.render();
  }

  render() {
    let inspiration = this.inspiration;
    console.log(inspiration);
    let htmlRender = `<a href="${this.href}"><article>
        <h2>${this.title}</h2>
        <h3>${this.subtitle}</h3>
        <slot name="image"></slot>
        <p class="days">
        ${this.days} days
        </p>
        <p class="kilometres">
        ${this.kilometres}  km
        </p>
        <p class="location">
        From ${this.start} to ${this.end}
        </p>
        <slot name="excerpt"></slot>
        </article></a>`;
    if (inspiration === "ardbeg") {
      htmlRender = `<a href="${this.href}"><article>
        <h2>${this.title}</h2>
        <h3>${this.subtitle}</h3>
        <slot name="excerpt"></slot>
        <slot name="image"></slot>
        <p class="kilometres">
            ${this.kilometres} km
        </p>
        <p class="days">
            ${this.days} days
        </p>
        <p class="location">
            From ${this.start} to ${this.end}
        </p>
        </article></a>`;
    } else if (inspiration === "glenlivet") {
      htmlRender = `<a href="${this.href}"><article>
        <h2>${this.title}</h2>
        <p class="kilometres">
          ${this.kilometres} km
        </p>
        <p class="days">
          ${this.days} days
        </p>
        <p class="location">
            From ${this.start} to ${this.end}
        </p>
        <p><slot name="excerpt"></slot></p>
        <h3>${this.subtitle}</h3>
        <figure><slot name="image"></slot></figure>
        </article></a>`;
    } else if (inspiration === "ben-nevis") {
      htmlRender = `<a href="${this.href}"><article>
      <h3>${this.subtitle}</h3>
        <h2>${this.title}</h2>
        <slot name="excerpt"></slot>
        <p class="days">
        ${this.days} days
        </p>
        <p class="kilometres">
        ${this.kilometres} km
        </p>
        <slot name="image"></slot>
        <p class="location">
        From ${this.start} to ${this.end}
        </p>
        </article></a>`;
    }
    // initially tried with templates defined outside class
    // but render template loses "this" reference? no attributes defined
    // not sure if it needed to be defined within class or what
    this.shadow.innerHTML = htmlRender;
  }
}
customElements.define("ww-label", Label);
