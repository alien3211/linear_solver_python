from django import forms

class LinearForm(forms.Form):
    row = forms.CharField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'variables split by ";"',
                    }),
                    required=False)