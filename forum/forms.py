# forum/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Resource
from .models import Doubt, User, OCRDoubtUpload

# OCR Upload Form
class OCRUploadForm(forms.ModelForm):
    class Meta:
        model = OCRDoubtUpload
        fields = ['image']  # Make sure this matches your model's ImageField
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        valid_mime_types = ['image/jpeg', 'image/png', 'image/jpg']
        if image.content_type not in valid_mime_types:
            raise ValidationError("Only JPEG and PNG files are allowed.")
        return image


# Faculty Suggestion Form
class FacultySuggestionForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['faculty_suggestion']
        widgets = {
            'faculty_suggestion': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }


# Custom User Signup Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'department', 'year', 'github_url', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        role = cleaned_data.get("role")

        if role == "faculty" and not (email and email.endswith(".ac.in")):
            raise forms.ValidationError("Faculty must use a college email ending in '.ac.in'.")
        return cleaned_data

    def _post_clean(self):
        super()._post_clean()
        role = self.cleaned_data.get("role")
        password = self.cleaned_data.get("password1")
        user = self.instance

        if role == "faculty":
            try:
                validate_password(password, user)
            except ValidationError as e:
                self.add_error('password1', e)


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'link', 'category']

# Ask Doubt Form
class DoubtForm(forms.ModelForm):
    is_public = forms.BooleanField(required=False, initial=True, label="Make this doubt public?")
    categories = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Doubt
        fields = ['title', 'description', 'code_snippet', 'categories', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'code_snippet': forms.Textarea(attrs={'rows': 6, 'class': 'font-monospace'}),
        }

    def __init__(self, *args, **kwargs):
        from .models import Category  # Avoid circular import
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()


# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        from .models import Comment
        model = Comment
        fields = ['content']
