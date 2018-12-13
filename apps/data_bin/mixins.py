from django.utils.decorators import decorator_from_middleware

from .middleware import BinItemDataEnrichFirstLevelMiddleware


class BinItemDataEnrichFirstLevelMixin(object):
    """
    Adds RequestLogMiddleware to any Django View by overriding as_view.
    """

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(BinItemDataEnrichFirstLevelMixin, cls).as_view(*args, **kwargs)
        view = decorator_from_middleware(BinItemDataEnrichFirstLevelMiddleware)(view)
        return view
