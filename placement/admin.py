from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv

from .models import Student, Report, ArchivedReport, Evaluation
from django.contrib.auth.models import Group, User

# Unregister default auth models
admin.site.unregister(Group)
admin.site.unregister(User)

# Customize admin site titles
admin.site.site_header = "OJT Placement Management System"
admin.site.site_title = "OJT Placement Management System"
admin.site.index_title = "Welcome to the OJT Management Dashboard"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id_number', 'get_full_name', 'time_of_log',
        'program', 'academic_year', 'company_placement',
        'company_address', 'ojt_start', 'ojt_end',
    )
    search_fields = (
        'id_number', 'last_name', 'first_name', 'program',
        'academic_year', 'company_placement', 'company_address'
    )
    list_filter = ('program', 'company_placement', 'academic_year')
    actions = ['export_as_csv']

    def get_full_name(self, obj):
        return f"{obj.last_name}, {obj.first_name} {obj.middle_name}"
    get_full_name.short_description = 'Full Name'

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=students.csv'

        writer = csv.writer(response)
        writer.writerow([
            'ID Number', 'Full Name', 'Program', 'Academic Year',
            'Company Placement', 'Company Address', 'OJT Start', 'OJT End'
        ])

        for student in queryset:
            writer.writerow([
                student.id_number,
                f"{student.last_name}, {student.first_name} {student.middle_name}",
                student.program,
                student.academic_year,
                student.company_placement,
                student.company_address,
                student.ojt_start,
                student.ojt_end
            ])

        return response
    export_as_csv.short_description = "Export selected students to CSV"



import csv
from django.http import HttpResponse
from django.utils.html import format_html
from django.contrib import admin

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id_number', 'get_full_name', 'download_column', 'uploaded_at')
    actions = ['export_as_csv']

    def id_number(self, obj):
        return obj.student.id_number
    id_number.short_description = 'ID Number'

    def get_full_name(self, obj):
        return obj.student.full_name
    get_full_name.short_description = 'Full Name'

    def download_column(self, obj):
        links = []
        if obj.file:
            links.append(f'<a href="{obj.file.url}" download style="color:lightblue;text-decoration: none;">Download File</a>')
        if obj.link:
            links.append(f'<a href="{obj.link}" target="_blank" style="color:green;text-decoration: none;">Open Link</a>')
        return format_html("<br>".join(links)) if links else "-"
    download_column.short_description = 'Report Access'

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=reports.csv'

        writer = csv.writer(response)
        writer.writerow(['ID Number', 'Full Name', 'File Available', 'Link Available', 'Uploaded At'])

        for obj in queryset:
            writer.writerow([
                obj.student.id_number,
                obj.student.full_name,
                'Yes' if obj.file else 'No',
                'Yes' if obj.link else 'No',
                obj.uploaded_at,
            ])
        return response

    export_as_csv.short_description = "Export selected reports to CSV"



    def delete_model(self, request, obj):
        self.archive_report(obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.archive_report(obj)
        super().delete_queryset(request, queryset)

    def archive_report(self, obj):
        ArchivedReport.objects.create(
            student_id=obj.student.id_number,
            full_name=obj.student.full_name,
            uploaded_at=obj.uploaded_at,
        )


import pytz
from django.utils.timezone import localtime

@admin.register(ArchivedReport)
class ArchivedReportAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'uploaded_at', 'archived_at', 'time_of_log',)
    search_fields = ('student_id', 'full_name')
    actions = ['export_as_csv']

    def time_of_log(self, obj):
        ph_tz = pytz.timezone('Asia/Manila')
        if obj.archived_at:
            # Convert archived_at to Philippine timezone
            ph_time = obj.archived_at.astimezone(ph_tz)
            # Format time like "11:39 AM"
            return ph_time.strftime('%I:%M %p')
        return '-'

    time_of_log.short_description = 'Time of Log'

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=archived_reports.csv'

        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Full Name', 'Uploaded At', 'Archived At', 'Time_of_Log',])

        ph_tz = pytz.timezone('Asia/Manila')

        for report in queryset:
            if report.archived_at:
                ph_time = report.archived_at.astimezone(ph_tz).strftime('%I:%M %p')
            else:
                ph_time = '-'

            writer.writerow([
                report.student_id,
                report.full_name,
                report.uploaded_at,
                report.archived_at,
                ph_time,
            ])
        return response

    export_as_csv.short_description = "Export selected archived reports to CSV"


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student_id_number', 'student_full_name', 'evaluator_name', 'company', 'final_grade', 'letter_grade', 'date_evaluated')
    search_fields = ('student__last_name', 'student__id_number', 'evaluator_name', 'company')
    list_filter = ('date_evaluated', 'company')
    actions = ['export_as_csv']

    def student_full_name(self, obj):
        return f"{obj.student.last_name}, {obj.student.first_name}"
    student_full_name.short_description = 'Student Name'

    def student_id_number(self, obj):
        return obj.student.id_number
    student_id_number.short_description = 'ID Number'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=Evaluation_{meta.verbose_name_plural}.csv'

        writer = csv.writer(response)
        writer.writerow([
            'ID Number', 'Full Name', 'Evaluator Name', 'Company',
            'Punctuality', 'Work Quality', 'Communication Skills',
            'Teamwork', 'Final Grade', 'letter_grade', 'Comments', 'Date Evaluated'
        ])
        for obj in queryset:
            writer.writerow([
                obj.student.id_number,
                f"{obj.student.last_name}, {obj.student.first_name}",
                obj.evaluator_name,
                obj.company,
                obj.punctuality,
                obj.work_quality,
                obj.communication_skills,
                obj.teamwork,
                obj.final_grade,
                obj.get_letter_grade(), 
                obj.comments,
                obj.date_evaluated,
            ])
        return response

    export_as_csv.short_description = "Export Selected to CSV"

    def letter_grade(self, obj):
        return obj.get_letter_grade()
    letter_grade.short_description = 'College Grade'