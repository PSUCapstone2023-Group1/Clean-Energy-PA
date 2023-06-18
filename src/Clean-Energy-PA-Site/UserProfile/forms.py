from django import forms


class EmailNotificationForm(forms.Form):
    email_notifications = forms.BooleanField(
        label="Enable Email Notifications", required=False
    )
