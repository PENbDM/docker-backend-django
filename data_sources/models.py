from django.db import models
from company.models import Company, CompanyMember


class DatabaseConnection(models.Model):
    DB_CHOICES = [
        ("postgres", "PostgreSQL"),
        ("mysql", "MySQL"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="database_connections"
    )

    name = models.CharField(max_length=100)
    db_type = models.CharField(max_length=20, choices=DB_CHOICES)

    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    database_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    encrypted_password = models.TextField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DataTable(models.Model):
    #DataTable represents a real database table that a company connected to Trevor.io.
    #Example: A company connects their PostgreSQL database.
    #Inside that database there are tables:
    # users
    #orders
    #products
    #payments
    #You need a Django model to store information about those tables.

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="data_tables"
    )

    connection = models.ForeignKey(
        DatabaseConnection,
        on_delete=models.CASCADE,
        related_name="tables"
    )

    table_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("connection", "table_name")

    def __str__(self):
        return self.display_name or self.table_name



class DataColumn(models.Model):
    #DataColumn represents a column inside a database table.
    #Example:You have a table:users with columns:

    #id
    #name
    #email
    #salary
    #created_at
    #Trevor.io needs to know these columns exist.


    table = models.ForeignKey(
        DataTable,
        on_delete=models.CASCADE,
        related_name="columns"
    )

    column_name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=100)

    is_sensitive = models.BooleanField(default=False)

    class Meta:
        unique_together = ("table", "column_name")

    def __str__(self):
        return f"{self.table.table_name}.{self.column_name}"


class TablePermission(models.Model):
    member = models.ForeignKey(
        CompanyMember,
        on_delete=models.CASCADE,
        related_name="table_permissions"
    )

    table = models.ForeignKey(
        DataTable,
        on_delete=models.CASCADE,
        related_name="permissions"
    )

    can_view = models.BooleanField(default=False)
    can_query = models.BooleanField(default=False)
    can_export = models.BooleanField(default=False)

    class Meta:
        unique_together = ("member", "table")

    def __str__(self):
        return f"{self.member.user.email} -> {self.table.table_name}"