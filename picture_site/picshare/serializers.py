import PIL
from io import BytesIO

from django.core.files.images import ImageFile

from rest_framework import serializers
from .models import CustomUser, Image, ExpiringLink
from os.path import splitext



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        tier = serializers.StringRelatedField(read_only=True)
        images = serializers.StringRelatedField(read_only=True)
        fields = ['images']


class ImageSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = ['images']
        read_only_fields = ('thumbnail_small', 'thumbnail_large')

    def get_images(self, obj):
        images = [obj.thumbnail_small.url]
        if obj.user.tier.thumbnail_size_large:
            images.append(obj.thumbnail_large.url)
        if obj.user.tier.original_size:
            images.append(obj.image.url)

        return images


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        sm, lg = user.tier.get_thumbnail_sizes
        picture = self.validated_data["image"]
        filename = splitext(picture.name)
        image = PIL.Image.open(picture)
        thumb_sm = image.copy()
        thumb_sm.thumbnail((sm, sm))
        thumb_lg = image.copy()
        thumb_lg.thumbnail((lg, lg))

        image_data = BytesIO()
        thumb_sm_data = BytesIO()
        thumb_lg_data = BytesIO()

        image.save(fp=image_data, format=picture.image.format)
        thumb_sm.save(fp=thumb_sm_data, format=picture.image.format)
        thumb_lg.save(fp=thumb_lg_data, format=picture.image.format)
        image_file = ImageFile(image_data, name=picture.name)
        thumb_sm_file = ImageFile(thumb_sm_data, name=filename[0] + '_sm' + filename[1])
        thumb_lg_file = ImageFile(thumb_lg_data, name=filename[0] + '_lg' + filename[1])

        return Image.objects.create(image=image_file, user=user, thumbnail_small=thumb_sm_file,
                                    thumbnail_large=thumb_lg_file)





class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ('link',)


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ('image', 'expires_in')

    def __init__(self, *args, **kwargs):
        super(ExpiringLinkCreateSerializer, self).__init__(*args, **kwargs)

        user = self.context.get('request').user
        images = Image.objects.filter(user=user)

        self.fields['image'].queryset = images
