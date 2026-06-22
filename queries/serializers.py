from rest_framework import serializers
from .models import SavedQuery,QueryRun,QueryResult


class SavedQuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedQuery
        fields = [
            "id",
            "company",
            "created_by",
            "connection",
            "name",
            "query_json",
            "generated_sql",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class QueryRunSerializer(serializers.ModelSerializer):

    class Meta:
        model = QueryRun
        fields = [
            "id",
            "company",
            "member",
            "connection",
            "saved_query",
            "sql",
            "status",
            "error",
            "created_at",
            "finished_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "finished_at",
        ]


class QueryResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = QueryResult
        fields = [
            "id",
            "query_run",
            "result_json",
            "row_count",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]