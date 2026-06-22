from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models  import DatabaseConnection,DataTable,DataColumn,TablePermission
from .serializers import DatabaseConnectionSerializer, DataTableSerializer, DataColumnSerializer, \
    TablePermissionSerializer
from .services import connect_to_database,get_tables,get_columns

class DatabaseConnectionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer= DatabaseConnectionSerializer(data=request.data)

        if serializer.is_valid():
            db_connection=serializer.save()
            connection = connect_to_database(db_connection)

            connection.close()
            return Response(
                DatabaseConnectionSerializer(db_connection).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class DataTableView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, connection_id):

        tables = DataTable.objects.filter(
            connection_id=connection_id
        )

        serializer = DataTableSerializer(
            tables,
            many=True
        )

        return Response(serializer.data)



class SyncTablesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, connection_id):

        db_connection = DatabaseConnection.objects.get(
            id=connection_id
        )

        connection = connect_to_database(db_connection)

        tables = get_tables(connection)

        synced_tables = []

        for table in tables:

            DataTable.objects.get_or_create(
                company=db_connection.company,
                connection=db_connection,
                table_name=table[0]
            )

            synced_tables.append(table[0])

        connection.close()

        return Response(
            {
                "message": "Tables synced successfully",
                "tables": synced_tables
            },
            status=status.HTTP_200_OK
        )




class DataColumnView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, table_id):

        columns = DataColumn.objects.filter(
            table_id=table_id
        )

        serializer = DataColumnSerializer(
            columns,
            many=True
        )

        return Response(serializer.data)




class SyncColumnsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, connection_id):

        db_connection = DatabaseConnection.objects.get(
            id=connection_id
        )

        connection = connect_to_database(db_connection)

        tables = DataTable.objects.filter(
            connection=db_connection
        )

        synced_columns = []

        for table in tables:

            columns = get_columns(
                connection,
                table.table_name
            )

            for column_name, data_type in columns:

                DataColumn.objects.get_or_create(
                    table=table,
                    column_name=column_name,
                    defaults={
                        "data_type": data_type
                    }
                )

                synced_columns.append({
                    "table": table.table_name,
                    "column": column_name,
                    "type": data_type
                })

        connection.close()

        return Response(
            {
                "message": "Columns synced successfully",
                "columns": synced_columns
            },
            status=status.HTTP_200_OK
        )




class TablePermissionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer= TablePermissionSerializer(data=request.data)
        if serializer.is_valid():
            table_permission=serializer.save()
            return Response(
                TablePermissionSerializer(table_permission).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )