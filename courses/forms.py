# courses/forms.py
from django import forms
from .models import Course, CustomUser

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'instructor', 'category', 
            'price', 'duration', 'thumbnail', 'is_paid', 
            'is_active', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter course description'
            }),
            'instructor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_paid': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        is_paid = self.cleaned_data.get('is_paid')
        
        if is_paid and price <= 0:
            raise forms.ValidationError("Paid courses must have a price greater than 0.")
        
        if not is_paid and price > 0:
            raise forms.ValidationError("Free courses must have a price of 0.")
        
        return price

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'})
        }