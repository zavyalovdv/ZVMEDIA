from uuid import uuid4
from pytils.translit import slugify

def unique_slugify_models(instance, pre_slug):
    """
    Автоматический генератор уникальных SLUG для моделей
    """
    model = instance.__class__
    unique_slug = slugify(pre_slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


def unique_slugify_forms(pre_slug):
    """
    Автоматический генератор уникальных SLUG
    """
    unique_slug = slugify(pre_slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug