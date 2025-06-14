from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

PROGRAM_CHOICES = [
    ('BSAIS', 'BSAIS'),
    ('BSIT', 'BSIT'),
    ('BSCRIM', 'BSCRIM'),
    ('BSOA', 'BSOA'),
    ('BEED', 'BEED'),
    ('BSED', 'BSED'),
    ('BSTM', 'BSTM'),
    
    # Add your other programs here
]

ACADEMIC_YEAR_CHOICES = [
    ('2021-2022', '2021-2022'),
    ('2023-2024', '2023-2024'),
    ('2024-2025', '2024-2025'),
    ('2026-2027', '2026-2027'),
    # Add other academic years as needed
]

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    time_of_log = models.DateTimeField(auto_now_add=True)
    program = models.CharField(max_length=50, choices=PROGRAM_CHOICES)
    academic_year = models.CharField(max_length=9, choices=ACADEMIC_YEAR_CHOICES)
    barangay = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    company_placement = models.CharField(max_length=100)
    company_address = models.CharField(max_length=150)
    designated = models.CharField(max_length=100)
    ojt_start = models.DateTimeField()
    ojt_end = models.DateTimeField()
    total_hours = models.IntegerField()

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name or ''}".strip()

    def __str__(self):
        return f"{self.id_number} - {self.full_name} ({self.program})"

class Report(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to='reports/', blank=True, null=True)  # Optional file
    link = models.URLField(blank=True, null=True)  # Optional link
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.id_number} - {self.student.full_name} Report"


class ArchivedReport(models.Model):
    student_id = models.CharField(max_length=20)
    full_name = models.CharField(max_length=150)
    file = models.FileField(upload_to='archived_reports/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField()
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived Report: {self.full_name} ({self.student_id})"


# models.py

class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    evaluator_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    date_evaluated = models.DateField(auto_now_add=True)

    punctuality = models.IntegerField(choices=[(i, i) for i in range(60, 99)])
    work_quality = models.IntegerField(choices=[(i, i) for i in range(60, 99)])
    communication_skills = models.IntegerField(choices=[(i, i) for i in range(60, 99)])
    teamwork = models.IntegerField(choices=[(i, i) for i in range(60, 99)])
    comments = models.TextField(blank=True)

    final_grade = models.DecimalField(max_digits=4, decimal_places=2, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        scores = [self.punctuality, self.work_quality, self.communication_skills, self.teamwork]
        self.final_grade = round(sum(scores) / len(scores), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Evaluation for {self.student.full_name}"

    def get_letter_grade(self):
        if self.final_grade >= 99:
            return '1.0'
        elif self.final_grade >= 95:
            return '1.3'
        elif self.final_grade >= 90:
            return '1.5'
        elif self.final_grade >= 85:
            return '2.0'
        elif self.final_grade >= 80:
            return '2.5'
        elif self.final_grade >= 75:
            return '3.0'
        else:
            return '5.0'

# models.py
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)

