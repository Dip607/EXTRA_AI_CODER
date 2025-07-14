from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Doubt


# Delay model imports using local imports to avoid circular dependency during startup

User = get_user_model()

# Choice fields (can also be imported from models later for DRY code)
ROLE_CHOICES = (
    ('student', 'Student'),
    ('faculty', 'Faculty'),
)

DEPARTMENT_CHOICES = (
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('ME', 'Mechanical'),
    ('CE', 'Civil'),
    ('EE', 'Electrical'),
)

YEAR_CHOICES = (
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
    (4, '4th Year'),
)

class FacultySuggestionForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['faculty_suggestion']
        widgets = {
            'faculty_suggestion': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    github_url = forms.URLField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role',
            'department',
            'year',
            'github_url',
        ]


class DoubtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Import Category model locally to prevent circular import at project startup
        from .models import Category
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()

    is_public = forms.BooleanField(required=False, initial=True, label="Make this doubt public?")
    categories = forms.ModelMultipleChoiceField(
        queryset=None,  # Will be filled in __init__
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        from .models import Doubt  # Import locally
        model = Doubt
        fields = ['title', 'description', 'code_snippet', 'categories', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'code_snippet': forms.Textarea(attrs={'rows': 6, 'class': 'font-monospace'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        from .models import Comment  # Local import
        model = Comment
        fields = ['content']
