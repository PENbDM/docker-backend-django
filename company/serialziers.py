from rest_framework import serializers
from .models import Company, CompanyMember


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "owner", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]


class CompanyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMember
        fields = [
            "id",
            "company",
            "user",
            "role",
            "joined_at",
        ]
        read_only_fields = ["id", "joined_at"]