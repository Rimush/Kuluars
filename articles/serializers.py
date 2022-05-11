from rest_framework import serializers
from .models import Article
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)
from taggit.models import Tag

class articles_serializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Article
        fields = ('id', 'category', 'author', 'source', 'important', 'image', 'image_signature', 'title', 'slug', 'fulltext', 'created', 'earlier', 'views', 'tags')

class tags_serializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
