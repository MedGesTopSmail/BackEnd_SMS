from django import forms
from MyAppApi.models import Mailing_List

class MailingListForm(forms.ModelForm):
    Mailing_List_Url = forms.FileField(required=True, label='Choose a file')

    class Meta:
        model = Mailing_List
        fields = ('Mailing_List_Url',)
        labels = {
            "Mailing_List_Url": "Choose a file",
        }