# navbar

Documents steps to implement a navigation bar (navbar) on the website.

See also:

[Django website notes](README.md)<br>
[Navigation bar notes](navbar.md)<br>
[Plans](../plans.md)<br>
[Defects](../defects.md)<br>
[Repository README](../README.md)

## Content and style

### Title and link

In [navbar.html](../www/ocm/website/templates/navbar.html) change from:

    <a class="navbar-brand" href="#">Navbar</a>

To: 
    <a class="navbar-brand" href="{% url 'home' %}">Open Circuit Maker</a>

The {% %} is for Django and the {% url 'home' %} will insert a link back to the website home page.

### Make the navbar dark

In [navbar.html](../www/ocm/website/templates/navbar.html) change from:

```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
```

To:

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
```

### Add a login item

In [navbar.html](../www/ocm/website/templates/navbar.html) change from:

```html
<li class="nav-item">
  <a class="nav-link disabled" aria-disabled="true">Disabled</a>
</li>
```

To:

```html
<li class="nav-item">
  <a class="nav-link" aria-disabled="true">Login</a>
</li>
```
