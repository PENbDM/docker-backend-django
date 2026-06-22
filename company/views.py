from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Company, CompanyMember
from .serialziers import CompanySerializer,CompanyMemberSerializer


class CompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            company = serializer.save(owner=request.user)

            CompanyMember.objects.create(
                company=company,
                user=request.user,
                role="owner"
            )

            return Response(
                CompanySerializer(company).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        companies = Company.objects.filter(owner=request.user)

        serializer = CompanySerializer(
            companies,
            many=True
        )

        return Response(serializer.data)


class CompanyMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        members = CompanyMember.objects.filter(
            company_id=company_id
        ).select_related("user", "company")

        serializer = CompanyMemberSerializer(
            members,
            many=True
        )

        return Response(serializer.data)

class CompanyMemberView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
        member=CompanyMember.objects.filter(
            user=user_id
        )
        serializer = CompanyMemberSerializer(
            member,
            many=True
        )

        return Response(serializer.data)