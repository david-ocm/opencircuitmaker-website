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

### Remove unused parts

In [navbar.html](../www/ocm/website/templates/navbar.html) remove:

```html
        <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
```

Also remove:
```html
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#">Home</a>
          </li>
```

### Add an FAQ item

In [navbar.html](../www/ocm/website/templates/navbar.html) change from:

```html
<li class="nav-item">
  <a class="nav-link disabled" aria-disabled="true">Disabled</a>
</li>
```

To:

```html
<li class="nav-item">
    <a class="nav-link" href = {% url 'faq' %}>FAQ</a>
</li>
```
In [views.py](../www/ocm/website/views.py) add:

```python
def faq(request):
    return render(request, 'faq.html', {})
```

In templates, create a file [faq.html](../www/ocm/website/templates/faq.html):

```html
{% extends 'base.html' %}

{% block content %}
<h1>Frequently asked questions</h1>
Why is this here?<br/>

{% endblock %}
```

In [urls.py](../www/ocm/website/urls.py) change urlpatterns thus:

```python
urlpatterns = [
    path('', views.home, name='home'),
    path('/faq', views.faq, name='faq'),
]
```

### Add a "view" for the FAQ item

Django uses a function referred to as a "view" for links.

In [navbar.html](../www/ocm/website/templates/navbar.html) change from: