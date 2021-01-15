from functools import partial
from graphene_django_extras.base_types import DjangoListObjectBase
from graphene_django_extras.utils import queryset_factory
from graphene_django_extras import DjangoListObjectField
from graphene_django.utils import maybe_queryset


class WithResolverDjangoListObjectField(DjangoListObjectField):
    """Allows to define a resolver for the list object field."""

    def list_resolver(self, resolver, manager, filterset_class, filtering_args, root, info, **kwargs):
        resolve_queryset = resolver(root, info, **kwargs)
        qs_factory = queryset_factory(manager, info.field_asts, info.fragments, **kwargs)

        qs = resolve_queryset & qs_factory  # merge querysets
        filter_kwargs = {k: v for k, v in kwargs.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs
        count = qs.count()

        return DjangoListObjectBase(
            count=count,
            results=maybe_queryset(qs),
            results_field_name=self.type._meta.results_field_name
        )


    def get_resolver(self, parent_resolver):
        return partial(
            self.list_resolver,
            parent_resolver,
            self.model._default_manager,
            self.filterset_class,
            self.filtering_args
        )
