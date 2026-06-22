from rest_framework import serializers
from .models import DatabaseConnection,DataColumn,DataTable,TablePermission

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=DatabaseConnection
        fields=['id','company','name','db_type','host','port','database_name',
                'username','encrypted_password','is_active']
        read_only_fields = [
            "id",
            "created_at",
        ]


class DataTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=DataTable
        fields=['id','company','connection',"table_name","display_name"]


class DataColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model=DataColumn
        fields=['table','column_name','data_type','is_sensitive']


class TablePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=TablePermission
        fields=['member','table','can_view','can_query','can_export']