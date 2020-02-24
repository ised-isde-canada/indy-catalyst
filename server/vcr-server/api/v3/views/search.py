import logging

from django.conf import settings
from django.http import Http404
from drf_haystack.filters import HaystackOrderingFilter
from drf_haystack.mixins import FacetMixin
from drf_haystack.viewsets import HaystackViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from haystack.query import RelatedSearchQuerySet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v2.models.Credential import Credential
from api.v2.models.Name import Name
from api.v2.models.Address import Address
from api.v2.models.Topic import Topic

from api.v3.search_filters import AutocompleteFilter, StatusFilter
from api.v3.serializers.search import (
    NameAutocompleteSerializer,
    AddressAutocompleteSerializer,
    AggregateAutocompleteSerializer,
)
from vcr_server.pagination import ResultLimitPagination

LOGGER = logging.getLogger(__name__)


class NameAutocompleteView(HaystackViewSet):
    """
    Return autocomplete results for a query string
    """

    permission_classes = (permissions.AllowAny,)
    pagination_class = ResultLimitPagination

    _swagger_params = [
        openapi.Parameter(
            "q", openapi.IN_QUERY, description="Query string", type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            "inactive",
            openapi.IN_QUERY,
            description="Show inactive credentials",
            type=openapi.TYPE_STRING,
            enum=["false", "true"],
            default=None,
        ),
        openapi.Parameter(
            "revoked",
            openapi.IN_QUERY,
            description="Show revoked credentials",
            type=openapi.TYPE_STRING,
            enum=["false", "true"],
            default="false",
        ),
    ]

    @swagger_auto_schema(
        manual_parameters=_swagger_params,
        responses={200: AggregateAutocompleteSerializer(many=True)},
    )
    def list(self, *args, **kwargs):
        print(" >>> calling autocomplete")
        ret = super(NameAutocompleteView, self).list(*args, **kwargs)
        print(" >>> autocomplete returns", ret)
        return ret

    retrieve = None
    index_models = [Address, Name, Topic]
    load_all = True
    serializer_class = AggregateAutocompleteSerializer
    filter_backends = (AutocompleteFilter, StatusFilter)
    ordering = "-score"
