from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-12 col-sm-6'),
                Column('email', css_class='col-12 col-sm-6'),
            ),
            Row(
                Column('first_name', css_class='col-12 col-sm-6'),
                Column('last_name', css_class='col-12 col-sm-6'),
            ),
            Row(
                Column('password1', css_class='col-12 col-sm-6'),
                Column('password2', css_class='col-12 col-sm-6'),
            ),
            Submit('submit', 'Register')
        )
