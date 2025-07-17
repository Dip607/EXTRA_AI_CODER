from django import forms
from .models import Submission
from .models import CodingContest

        
class CodingContestForm(forms.ModelForm):
    class Meta:
        model = CodingContest
        fields = ['title', 'description', 'start_time', 'end_time']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code', 'language']