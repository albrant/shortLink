from django import forms


class UrlForm(forms.Form):
    url = forms.URLField(
        label='Длинная ссылка:'
    )
    ttl = forms.IntegerField(
        label='Время жизни (в минутах)'
    )
