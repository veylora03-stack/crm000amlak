from rest_framework import serializers

from .models import MatchScore, Property, PropertyImage, PropertyStatus, PublishStatus


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = [
            'public_id',
            'image',
            'thumbnail',
            'alt_text',
            'sort_order',
            'is_primary',
            'created_at'
        ]
        read_only_fields = ['public_id', 'thumbnail', 'created_at']


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    owner_client_name = serializers.CharField(source='owner_client.full_name', read_only=True, default='')
    assigned_agent_name = serializers.CharField(source='assigned_agent.full_name', read_only=True, default='')

    class Meta:
        model = Property
        fields = [
            'public_id',
            'code',
            'title',
            'slug',
            'property_type',
            'listing_type',
            'status',
            'publish_status',
            'price',
            'deposit_amount',
            'rent_amount',
            'land_area',
            'building_area',
            'bedrooms',
            'bathrooms',
            'parking_count',
            'floor_number',
            'total_floors',
            'year_built',
            'address',
            'province',
            'city',
            'district',
            'neighborhood',
            'latitude',
            'longitude',
            'description',
            'amenities',
            'images',
            'owner_client',
            'owner_client_name',
            'assigned_agent',
            'assigned_agent_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['public_id', 'slug', 'created_at', 'updated_at']


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'code',
            'title',
            'property_type',
            'listing_type',
            'status',
            'publish_status',
            'price',
            'deposit_amount',
            'rent_amount',
            'land_area',
            'building_area',
            'bedrooms',
            'bathrooms',
            'parking_count',
            'floor_number',
            'total_floors',
            'year_built',
            'address',
            'province',
            'city',
            'district',
            'neighborhood',
            'latitude',
            'longitude',
            'description',
            'amenities',
            'owner_client',
            'assigned_agent'
        ]

    def validate(self, attrs):
        price = attrs.get('price', 0)
        deposit_amount = attrs.get('deposit_amount', 0)
        rent_amount = attrs.get('rent_amount', 0)

        if price < 0:
            raise serializers.ValidationError('قیمت نمی‌تواند منفی باشد.')

        if deposit_amount < 0:
            raise serializers.ValidationError('مبلغ رهن نمی‌تواند منفی باشد.')

        if rent_amount < 0:
            raise serializers.ValidationError('مبلغ اجاره نمی‌تواند منفی باشد.')

        return attrs


class PropertyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'code',
            'title',
            'property_type',
            'listing_type',
            'status',
            'publish_status',
            'price',
            'deposit_amount',
            'rent_amount',
            'land_area',
            'building_area',
            'bedrooms',
            'bathrooms',
            'parking_count',
            'floor_number',
            'total_floors',
            'year_built',
            'address',
            'province',
            'city',
            'district',
            'neighborhood',
            'latitude',
            'longitude',
            'description',
            'amenities',
            'owner_client',
            'assigned_agent'
        ]

    def validate(self, attrs):
        price = attrs.get('price', 0)
        deposit_amount = attrs.get('deposit_amount', 0)
        rent_amount = attrs.get('rent_amount', 0)

        if price < 0:
            raise serializers.ValidationError('قیمت نمی‌تواند منفی باشد.')

        if deposit_amount < 0:
            raise serializers.ValidationError('مبلغ رهن نمی‌تواند منفی باشد.')

        if rent_amount < 0:
            raise serializers.ValidationError('مبلغ اجاره نمی‌تواند منفی باشد.')

        return attrs


class PropertyListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    assigned_agent_name = serializers.CharField(source='assigned_agent.full_name', read_only=True, default='')

    class Meta:
        model = Property
        fields = [
            'public_id',
            'code',
            'title',
            'property_type',
            'listing_type',
            'status',
            'publish_status',
            'price',
            'city',
            'district',
            'building_area',
            'bedrooms',
            'primary_image',
            'assigned_agent_name',
            'created_at'
        ]

    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True, is_deleted=False).first()
        if image:
            return PropertyImageSerializer(image).data
        return None


class MatchScoreSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    property_title = serializers.CharField(source='property.title', read_only=True)

    class Meta:
        model = MatchScore
        fields = [
            'public_id',
            'client',
            'client_name',
            'property',
            'property_title',
            'score',
            'matched_fields',
            'created_at'
        ]
