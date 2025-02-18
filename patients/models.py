from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="patients",
        verbose_name="Associated User"
    )  # Link Patient to a User

    name = models.CharField(max_length=255, verbose_name="Patient Name")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other', verbose_name="Gender")
    diagnosis = models.TextField(verbose_name="Diagnosis")

    medical_report = models.FileField(
        upload_to='medical_reports/', 
        blank=True, 
        null=True, 
        verbose_name="Medical Report"
    )  # Allow null for optional report

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")

    def __str__(self):
        return f"{self.name} (Age: {self.age})"

    # ✅ Get the correct URL for S3 or local storage
    def get_medical_report_url(self):
        if self.medical_report:
            return self.medical_report.url  # Returns S3 or local file URL
        return ""

    class Meta:
        ordering = ["-created_at"]  # Show latest patients first
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
