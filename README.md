# What issue does this demonstrate

This repo exercises various ModelAdmin custom models that had been
working up until commit "[80cc70b7ce6f5013fcc69ea8878dd4ab79d3ae1d](https://github.com/wagtail/wagtail/commit/80cc70b7ce6f5013fcc69ea8878dd4ab79d3ae1d)
Instantiate edit_handler and form once in ModelAdmin views"

There appears to be a change in how choosers interact with costom edit
handlers. If we don't declare an edit_handler, all these models wwork
fine. But if we customize the panels and then declare the edit_handler
to be a TabbedInterface, we get stack traces like the one below for
any model that has an image, document, or page chooser in its admin
interface.

As far as I can see, we are setting up things as discussed in the
ModelAdmin customization docs:
https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/create_edit_delete_views.html

```
Template error:
In template /code/wagtail/wagtail/admin/templates/wagtailadmin/edit_handlers/multi_field_panel.html, error at line 5
   'NoneType' object has no attribute '_meta'
   1 : <fieldset>
   2 :     <legend>{{ self.heading }}</legend>
   3 :     <ul class="fields">
   4 :         {% for child in self.children %}
   5 :             <li class="{{ child.classes|join:" " }}"> {{ child.render_as_field }} </li>
   6 :         {% endfor %}
   7 :     </ul>
   8 : </fieldset>
   9 :

Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/django/core/handlers/exception.py", line 47, in inner
    response = get_response(request)
  File "/usr/local/lib/python3.7/site-packages/django/core/handlers/base.py", line 202, in _get_response
    response = response.render()
  File "/usr/local/lib/python3.7/site-packages/django/template/response.py", line 105, in render
    self.content = self.rendered_content
  File "/usr/local/lib/python3.7/site-packages/django/template/response.py", line 83, in rendered_content
    return template.render(context, self._request)
  File "/usr/local/lib/python3.7/site-packages/django/template/backends/django.py", line 61, in render
    return self.template.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 170, in render
    return self._render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 162, in _render
    return self.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/loader_tags.py", line 150, in render
    return compiled_parent._render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 162, in _render
    return self.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/loader_tags.py", line 150, in render
    return compiled_parent._render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 162, in _render
    return self.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/loader_tags.py", line 150, in render
    return compiled_parent._render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 162, in _render
    return self.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/loader_tags.py", line 62, in render
    result = block.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/loader_tags.py", line 62, in render
    result = block.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/loader_tags.py", line 62, in render
    result = block.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 988, in render
    output = self.filter_expression.resolve(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 671, in resolve
    obj = self.var.resolve(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 796, in resolve
    value = self._resolve_lookup(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 858, in _resolve_lookup
    current = current()
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 238, in render_form_content
    return mark_safe(self.render_as_object() + self.render_missing_fields())
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 206, in render_as_object
    return self.render()
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 310, in render
    'self': self
  File "/usr/local/lib/python3.7/site-packages/django/template/loader.py", line 62, in render_to_string
    return template.render(context, request)
  File "/usr/local/lib/python3.7/site-packages/django/template/backends/django.py", line 61, in render
    return self.template.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 170, in render
    return self._render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 162, in _render
    return self.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/defaulttags.py", line 211, in render
    nodelist.append(node.render_annotated(context))
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 988, in render
    output = self.filter_expression.resolve(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 671, in resolve
    obj = self.var.resolve(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 796, in resolve
    value = self._resolve_lookup(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 858, in _resolve_lookup
    current = current()
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 206, in render_as_object
    return self.render()
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 310, in render
    'self': self
  File "/usr/local/lib/python3.7/site-packages/django/template/loader.py", line 62, in render_to_string
    return template.render(context, request)
  File "/usr/local/lib/python3.7/site-packages/django/template/backends/django.py", line 61, in render
    return self.template.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 170, in render
    return self._render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 162, in _render
    return self.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/defaulttags.py", line 211, in render
    nodelist.append(node.render_annotated(context))
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 988, in render
    output = self.filter_expression.resolve(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 671, in resolve
    obj = self.var.resolve(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 796, in resolve
    value = self._resolve_lookup(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 858, in _resolve_lookup
    current = current()
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 206, in render_as_object
    return self.render()
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 310, in render
    'self': self
  File "/usr/local/lib/python3.7/site-packages/django/template/loader.py", line 62, in render_to_string
    return template.render(context, request)
  File "/usr/local/lib/python3.7/site-packages/django/template/backends/django.py", line 61, in render
    return self.template.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 170, in render
    return self._render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 162, in _render
    return self.nodelist.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 938, in render
    bit = node.render_annotated(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/defaulttags.py", line 211, in render
    nodelist.append(node.render_annotated(context))
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 905, in render_annotated
    return self.render(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 988, in render
    output = self.filter_expression.resolve(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 671, in resolve
    obj = self.var.resolve(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 796, in resolve
    value = self._resolve_lookup(context)
  File "/usr/local/lib/python3.7/site-packages/django/template/base.py", line 858, in _resolve_lookup
    current = current()
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 572, in render_as_field
    instance_obj = self.get_chosen_item()
  File "/code/wagtail/wagtail/admin/edit_handlers.py", line 561, in get_chosen_item
    field = self.instance._meta.get_field(self.field_name)

Exception Type: AttributeError at /admin/home/relatedlink/create/
Exception Value: 'NoneType' object has no attribute '_meta'

```


# How to use this repo

The easy way would probably be to copy home/models.py and
home/wagtail_hooks.py into one of the apps in Bakerydemo, and carry on
developing however you currently do.

What I wanted to be able to do was to substitute this repository for
the bakerydemo repository while using
https://github.com/wagtail/docker-wagtail-develop

Currently this isn't very smooth. What I do to make things work is to:
  1. Clone this repo into your checkout of https://github.com/wagtail/docker-wagtail-develop
     parallel to the directories for wagtail, libs, and bakerydemo
  2. cp Docker.backend ../
  3. cp docker-compose-maissue.yml ../
  4. docker-compose -f docker-compose-maissue.yml --build up
