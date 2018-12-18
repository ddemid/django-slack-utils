from django import forms


class CommandForm(forms.Form):
    token = forms.CharField()
    team_id = forms.CharField(required=False)
    team_domain = forms.CharField(required=False)
    enterprise_id = forms.CharField(required=False)
    enterprise_name = forms.CharField(required=False)
    channel_id = forms.CharField(required=False)
    channel_name = forms.CharField(required=False)
    user_id = forms.CharField()
    user_name = forms.CharField()
    command = forms.CharField()
    text = forms.CharField()
    response_url = forms.URLField()
    trigger_id = forms.CharField()
