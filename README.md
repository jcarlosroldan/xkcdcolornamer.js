# XKCD color namer

This is a simple JS library to get the name of a RGB color.

```html
<script type="text/javascript" src="xkcdcolornamer.min.js"></script>
```

```js
const colorNamer = new ColorNamer();
colorNamer.name(0, 130, 130)  // returns "teal"
colorNamer.name(120, 128, 0)  // returns "olive"
colorNamer.name(0, 40, 0)  // returns "neon green"
```

It was built by training a simple neural network with 4 layers with [3 x 9 x 27 x 128] weights, to keep it lightweight but effective enough to identify the colors. After training, a wrapper was built to serve it in JS.
