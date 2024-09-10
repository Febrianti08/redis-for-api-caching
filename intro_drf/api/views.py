from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Institutions, Metadata, Reports
from .serializers import InstitutionsSerializer, MetadataSerializer, ReportsSerializer
from django.core.cache import cache
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


class CachedListView(ListAPIView):
    """
    This class handles the caching, filtering, and response serialization. It uses the cache_key_prefix to ensure unique cache keys for each view.
    """
    cache_key_prefix = ''  # To be set in subclasses

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        # Apply filters based on request parameters
        for param, value in query_params.items():
            # Split the value by commas, or handle a single value
            value_list = value.split(',') if ',' in value else [value]
            if param == 'name':
                queryset = queryset.filter(
                    Q(top_sellers__contains=[{'name': value}]) | Q(top_buyers__contains=[{'name': value}])
                )
            else:
                # Build a Q object that combines multiple icontains filters
                q_objects = Q()
                for v in value_list:
                    # The ** operator is used to unpack the dictionary into keyword arguments for the Q object.
                    q_objects |= Q(**{f"{param}__icontains": v})
                
                queryset = queryset.filter(q_objects)
        return queryset

    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'{self.cache_key_prefix}-{query_params}'
        result = cache.get(cache_key)

        if not result:
            print('Hitting DB')
            result = self.get_queryset()
            cache.set(cache_key, result, 60)
        else:
            print('Cache retrieved!')

        result = self.serializer_class(result, many=True)
        return Response(result.data)

class InstitutionsView(CachedListView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer
    permission_classes = [IsAuthenticated,]
    cache_key_prefix = 'institution-trade'


class MetadataView(CachedListView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [IsAuthenticated,]
    cache_key_prefix = 'metadata'


class ReportsView(CachedListView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [IsAuthenticated,]
    cache_key_prefix = 'reports'