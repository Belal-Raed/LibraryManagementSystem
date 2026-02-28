
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='book_status')
def book_status(book):
    if book.is_available:
        return mark_safe('<span class="badge bg-success">Available</span>')
    return mark_safe('<span class="badge bg-danger">Fully Borrowed</span>')


@register.filter(name='star_range')
def star_range(value):
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter(name='empty_star_range')
def empty_star_range(value):
    try:
        return range(5 - int(value))
    except (ValueError, TypeError):
        return range(5)
