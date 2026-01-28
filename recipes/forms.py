from django import forms


class UserForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )


class RecipeForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Enter recipe title"})
    )

    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter ingredients separated by commas"})
    )

    steps = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter steps separated by commas"})
    )

    tags = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Enter tags separated by commas"})
    )
