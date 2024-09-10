# from django.shortcuts import render
# from rest_framework.generics import ListAPIView
# from django.core.cache import cache
# from rest_framework.response import Response
# from django.db.models import Q


# class CachedListView(ListAPIView):
#     cache_key_prefix = ''  # To be set in subclasses

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query_params = self.request.query_params

#         # Apply filters based on request parameters
#         for param, value in query_params.items():
#             if param == 'name':
#                 queryset = queryset.filter(
#                     Q(top_sellers__contains=[{'name': value}]) | Q(top_buyers__contains=[{'name': value}])
#                 )
#             else:
#                 filter_kwargs = {f"{param}__icontains": value}
#                 queryset = queryset.filter(**filter_kwargs)

#         return queryset

#     def list(self, request):
#         query_params = request.query_params.urlencode()
#         cache_key = f'{self.cache_key_prefix}-{query_params}'
#         result = cache.get(cache_key)

#         if not result:
#             print('Hitting DB')
#             result = self.get_queryset()
#             cache.set(cache_key, result, 60)
#         else:
#             print('Cache retrieved!')

#         result = self.serializer_class(result, many=True)
#         return Response(result.data)

# from .models import Institutions, Metadata, Reports
# from .serializers import InstitutionsSerializer, MetadataSerializer, ReportsSerializer


# class InstitutionsView(CachedListView):
#     queryset = Institutions.objects.all()
#     serializer_class = InstitutionsSerializer
#     cache_key_prefix = 'institution-trade'


# class MetadataView(CachedListView):
#     queryset = Metadata.objects.all()
#     serializer_class = MetadataSerializer
#     cache_key_prefix = 'metadata'


# class ReportsView(CachedListView):
#     queryset = Reports.objects.all()
#     serializer_class = ReportsSerializer
#     cache_key_prefix = 'reports'

from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Institutions, Metadata, Reports
from .serializers import InstitutionsSerializer, MetadataSerializer, ReportsSerializer
from django.core.cache import cache
from rest_framework.response import Response
from django.db.models import Q


# Create view for API Institutions
class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        for param, value in query_params.items():
            if param == 'name':
                # Apply filter to both top_sellers and other_sellers JSON columns
                queryset = queryset.filter(
                    Q(top_sellers__contains=[{'name': value}]) | Q(top_buyers__contains=[{'name': value}])
                )
            else:
                # Generic filtering for other fields
                # filter_kwargs = {f"{param}__icontains": value}
                queryset = queryset.filter({f"{param}__icontains": value})
        
        return queryset


    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'institution-trade-{query_params}'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)

        return Response(result.data)  # Return the serialized data as a response
    
# Create view for API Metadata
class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        for param, value in query_params.items():
            filter_kwargs = {f"{param}__icontains": value}
            queryset = queryset.filter(**filter_kwargs)
        
        return queryset


    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'metadata-{query_params}'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)

        return Response(result.data)  # Return the serialized data as a response
    
# Create view for API Reports
class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        for param, value in query_params.items():
            filter_kwargs = {f"{param}__icontains": value}
            queryset = queryset.filter(**filter_kwargs)
        
        return queryset


    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'reports-{query_params}'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)

        return Response(result.data)  # Return the serialized data as a response