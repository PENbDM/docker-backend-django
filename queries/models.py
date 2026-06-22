from django.db import models
from company.models import Company, CompanyMember
from data_sources.models import DatabaseConnection


class SavedQuery(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="saved_queries"
    )
    created_by = models.ForeignKey(
        CompanyMember,
        on_delete=models.CASCADE,
        related_name="saved_queries"
    )
    connection = models.ForeignKey(
        DatabaseConnection,
        on_delete=models.CASCADE,
        related_name="saved_queries"
    )

    name = models.CharField(max_length=255)
    query_json = models.JSONField()
    generated_sql = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class QueryRun(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="query_runs"
    )
    member = models.ForeignKey(
        CompanyMember,
        on_delete=models.CASCADE,
        related_name="query_runs"
    )
    connection = models.ForeignKey(
        DatabaseConnection,
        on_delete=models.CASCADE,
        related_name="query_runs"
    )
    saved_query = models.ForeignKey(
        SavedQuery,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="runs"
    )

    sql = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    error = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"QueryRun {self.id} - {self.status}"


class QueryResult(models.Model):
    query_run = models.OneToOneField(
        QueryRun,
        on_delete=models.CASCADE,
        related_name="result"
    )

    result_json = models.JSONField()
    row_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for QueryRun {self.query_run.id}"