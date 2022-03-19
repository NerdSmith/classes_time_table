from django import forms


class ScheduleInpForm(forms.Form):
    file = forms.FileField(required=True)
