from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import SavedQuery,QueryRun,QueryResult
from .serializers import SavedQuerySerializer,QueryRunSerializer,QueryResultSerializer


class SavedQueryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SavedQuerySerializer(
            data=request.data
        )

        if serializer.is_valid():

            query = serializer.save()

            return Response(
                SavedQuerySerializer(query).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class SavedQueryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):

        queries = SavedQuery.objects.filter(
            company_id=company_id
        )

        serializer = SavedQuerySerializer(
            queries,
            many=True
        )

        return Response(serializer.data)




class QueryRunView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = QueryRunSerializer(
            data=request.data
        )

        if serializer.is_valid():

            query_run = serializer.save()

            return Response(
                QueryRunSerializer(query_run).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class QueryRunListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):

        runs = QueryRun.objects.filter(
            company_id=company_id
        )

        serializer = QueryRunSerializer(
            runs,
            many=True
        )

        return Response(serializer.data)


class QueryResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = QueryResultSerializer(
            data=request.data
        )

        if serializer.is_valid():

            result = serializer.save()

            return Response(
                QueryResultSerializer(result).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class QueryResultListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, query_run_id):

        result = QueryResult.objects.get(
            query_run_id=query_run_id
        )

        serializer = QueryResultSerializer(result)

        return Response(serializer.data)
