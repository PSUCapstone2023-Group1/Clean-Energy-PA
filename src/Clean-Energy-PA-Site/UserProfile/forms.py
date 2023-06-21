from django import forms


class EmailNotificationPreferenceForm(forms.Form):
    email_notifications = forms.BooleanField(
        initial=True, label="Enable Email Notifications", required=False
    )
