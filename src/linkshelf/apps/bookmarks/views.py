from rest_framework import serializers, status, pagination
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from linkshelf.apps.bookmarks import selectors


class ListBookmarksView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'bookmarks/test.html'

    def get(self, request):
        return Response({'hello': 'world'})


class StringListField(serializers.Field):
    def to_internal_value(self, data):
        return data.split(',')

    def to_representation(self, value):
        return value


class ListBookmarks(APIView):

    class Pagination(pagination.CursorPagination):
            page_size = 4
            ordering = '-created_at'
            cursor_query_param = 'c'

    class ListBookmarkSerializer(serializers.Serializer):
        id = serializers.CharField()
        url = serializers.URLField()
        created_at = serializers.DateTimeField()
        tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class FilterSerializer(serializers.Serializer):
        tags = StringListField(required=False)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        paginator = self.Pagination()

        return paginator.get_paginated_response(
            data=self.ListBookmarkSerializer(
                many=True,
                instance=paginator.paginate_queryset(
                    queryset=selectors.get_all_bookmarks(filters=filters_serializer.data),
                    request=request,
                    view=self
                ),
            ).data
        )
