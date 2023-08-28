from django import forms


class LoginForm(forms.Form):
    """
    Login form.
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre de usuario",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control"
            }
        ))
