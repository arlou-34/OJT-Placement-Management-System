from django import forms
from django.contrib.auth.models import User
from .models import Student, Report
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        exclude = ['user', 'time_of_log']

        widgets = {
            'ojt_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ojt_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ReportUploadForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['file', 'link']  # allow uploading file OR submitting link

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        link = cleaned_data.get('link')

        if not file and not link:
            raise forms.ValidationError("You must upload a file or provide a link.")
        if file and link:
            raise forms.ValidationError("Please provide either a file or a link, not both.")
        return cleaned_data




class CompanyLoginForm(forms.Form):
    company_name = forms.CharField(label='Company Name', max_length=150)



from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'student',
            'evaluator_name',
            'company',
            'punctuality',
            'work_quality',
            'communication_skills',
            'teamwork',
            'comments',
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional comments'}),
        }
        labels = {
            'student': 'Student',
            'evaluator_name': 'Evaluator Name',
            'company': 'Company',
            'punctuality': 'Punctuality (60-98)',
            'work_quality': 'Work Quality (60-98)',
            'communication_skills': 'Communication Skills (60-98)',
            'teamwork': 'Teamwork (60-98)',
            'comments': 'Additional Comments',
        }
