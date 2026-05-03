from django import forms
from .models import Course, Material


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'price', 'is_active']


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'material_type', 'pdf_file', 'video_url']

    def clean(self):
        cleaned_data = super().clean()
        material_type = cleaned_data.get('material_type')
        pdf_file = cleaned_data.get('pdf_file')
        video_url = cleaned_data.get('video_url')

        if material_type == 'pdf' and not pdf_file:
            raise forms.ValidationError('Please upload a PDF file.')
        if material_type == 'video' and not video_url:
            raise forms.ValidationError('Please provide a video URL.')

        return cleaned_data
