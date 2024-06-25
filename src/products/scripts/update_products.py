from src.products.models import ProductGroup as pg
from loguru import logger


def run():
    group = pg.objects.get(pk=5)
    group.pk = 6
    group.save()
    logger.success("group id before:> {}", group
                   .id, feature="f-strings")
    logger.success("group id before:> {}", group
                   .id, feature="f-strings")
    # for g in groups:
    # g.id += 1
    # g.save(force_update=True)
    # logger.success("group id after:> {}", g.id, feature="f-strings")
