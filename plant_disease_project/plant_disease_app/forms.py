from django import forms


class PredictionForm(forms.Form):
    upload_image = forms.FileField()
    