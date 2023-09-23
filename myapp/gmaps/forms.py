from django import forms
from .models import Gmap, User

class GmapForm(forms.ModelForm):
    class Meta:
        model = Gmap
        fields = ['title', 'comment', 'latitude', 'longitude', 'picture', 'magic_word', 'user']

    latitude = forms.FloatField(widget=forms.HiddenInput(attrs={'id': 'gmap_latitude'}))
    longitude = forms.FloatField(widget=forms.HiddenInput(attrs={'id': 'gmap_longitude'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'id': 'gmap_title', 'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'id': 'gmap_comment', 'class': 'form-control', 'size': '40x4'}))
    magic_word = forms.CharField(required=False, initial="", widget=forms.TextInput(attrs={'id': 'magic_word', 'class': 'form-control'}))
    picture = forms.ImageField(widget=forms.FileInput(attrs={'id': 'picture', 'class': 'form-control'}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2051)))
    class Meta:
        model = User
        fields = ['email', 'username', 'birth', 'password']

class BirthDateForm(forms.Form):
    birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2051)))
