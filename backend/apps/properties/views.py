from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import IsAgentOrAbove
from apps.core.responses import success_response
from apps.core.viewsets import StandardModelViewSet

from .models import MatchScore, Property, PropertyImage
from .serializers import (
    MatchScoreSerializer,
    PropertyCreateSerializer,
    PropertyImageSerializer,
    PropertyListSerializer,
    PropertySerializer,
    PropertyUpdateSerializer
)


class PropertyFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['property_type', 'listing_type', 'status', 'publish_status', 'city', 'district', 'assigned_agent']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset

        from django.db.models import Q
        return queryset.filter(
            Q(code__icontains=value) |
            Q(title__icontains=value) |
            Q(address__icontains=value) |
            Q(city__icontains=value) |
            Q(district__icontains=value) |
            Q(neighborhood__icontains=value)
        )


class PropertyViewSet(StandardModelViewSet):
    queryset = Property.active_objects.all().select_related(
        'owner_client', 'assigned_agent', 'created_by'
    ).prefetch_related('images')
    permission_classes = [IsAuthenticated, IsAgentOrAbove]
    filterset_class = PropertyFilter
    search_fields = ['code', 'title', 'address', 'city']
    ordering_fields = ['created_at', 'updated_at', 'price', 'building_area', 'title']
    lookup_field = 'public_id'
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return PropertyCreateSerializer
        if self.action in ['update', 'partial_update']:
            return PropertyUpdateSerializer
        if self.action == 'list':
            return PropertyListSerializer
        return PropertySerializer

    def perform_create(self, serializer):
        property_obj = serializer.save(created_by=self.request.user)

        images = self.request.FILES.getlist('images')
        for index, image in enumerate(images):
            PropertyImage.objects.create(
                property=property_obj,
                image=image,
                sort_order=index,
                is_primary=(index == 0)
            )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def images(self, request, public_id=None):
        property_obj = self.get_object()
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({
                'success': False,
                'data': None,
                'meta': None,
                'errors': [{'code': 'VALIDATION_ERROR', 'field': 'image', 'message': 'فایل تصویر الزامی است.'}]
            }, status=status.HTTP_400_BAD_REQUEST)

        from apps.core.validators import validate_image_extension, validate_file_size

        try:
            validate_image_extension(image_file)
            validate_file_size(image_file)
        except Exception as e:
            return Response({
                'success': False,
                'data': None,
                'meta': None,
                'errors': [{'code': 'VALIDATION_ERROR', 'field': 'image', 'message': str(e)}]
            }, status=status.HTTP_400_BAD_REQUEST)

        current_count = property_obj.images.filter(is_deleted=False).count()
        is_primary = request.data.get('is_primary', 'false').lower() == 'true'

        if is_primary:
            property_obj.images.filter(is_primary=True).update(is_primary=False)

        property_image = PropertyImage.objects.create(
            property=property_obj,
            image=image_file,
            alt_text=request.data.get('alt_text', ''),
            sort_order=current_count,
            is_primary=is_primary
        )

        return Response(success_response(PropertyImageSerializer(property_image).data), status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def publish(self, request, public_id=None):
        property_obj = self.get_object()
        property_obj.publish_status = 'Published'
        property_obj.updated_by = request.user
        property_obj.save(update_fields=['publish_status', 'updated_by', 'updated_at'])

        return Response(success_response(PropertySerializer(property_obj).data))

    @action(detail=True, methods=['post'])
    def archive(self, request, public_id=None):
        property_obj = self.get_object()
        property_obj.publish_status = 'Archived'
        property_obj.updated_by = request.user
        property_obj.save(update_fields=['publish_status', 'updated_by', 'updated_at'])

        return Response(success_response(PropertySerializer(property_obj).data))

    @action(detail=True, methods=['get'])
    def matches(self, request, public_id=None):
        property_obj = self.get_object()
        match_scores = MatchScore.active_objects.filter(property=property_obj).select_related('client', 'property').order_by('-score')[:20]

        data = MatchScoreSerializer(match_scores, many=True).data

        return Response(success_response(data))
