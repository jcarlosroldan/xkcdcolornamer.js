# XKCD color namer

This is a simple JS library to get the name of a RGB color.

```html
<script type="text/javascript" src="xkcdcolornamer.min.js"></script>
```

```js
const colorNamer = new ColorNamer();
colorNamer.name(0, 130, 130)  // teal
colorNamer.name(120, 128, 0)  // olive
colorNamer.name(0, 40, 0)  // neon green
```