from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Post, Profile, Comment, Subscribe


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('published_date', 'user')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'phone']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']


class RegistrationForm(forms.Form):
    city_choice = [
        ("Dnipro", "Dnipro"),
        ("Kyiv", "Kyiv"),
        ("Kharkiv", "Kharkiv"),
        ("Odesa", "Odesa"),
        ("Lviv", "Lviv"),
        ("Zaporizhzhia", "Zaporizhzhia"),
        ("Kryvyi Rih", "Kryvyi Rih"),
        ("Mykolaiv", "Mykolaiv"),
        ("Mariupol", "Mariupol"),
        ("Luhansk", "Luhansk"),
        ("Vinnytsia", "Vinnytsia"),
        ("Kherson", "Kherson"),
        ("Poltava", "Poltava"),
        ("Chernihiv", "Chernihiv"),
        ("Cherkasy", "Cherkasy"),
        ("Sumy", "Sumy"),
        ("Zhytomyr", "Zhytomyr"),
        ("Ivano-Frankivsk", "Ivano-Frankivsk"),
        ("Ternopil", "Ternopil"),
        ("Chernivtsi", "Chernivtsi"),
        ("Rivne", "Rivne"),
        ("Kropyvnytskyi", "Kropyvnytskyi"),
        ("Khmelnytskyi", "Khmelnytskyi"),
        ("Uzhhorod", "Uzhhorod")
    ]
    gender_choice = [('M', 'Male'), ('F', 'Female'),]

    Username = forms.CharField(max_length=20)
    First_name = forms.CharField(max_length=20)
    Last_name = forms.CharField(max_length=20)
    Gender = forms.ChoiceField(choices=gender_choice)
    Mail = forms.EmailField(max_length=15)
    Phone = forms.CharField(widget=forms.NumberInput())
    Country = forms.CharField(max_length=20)
    City = forms.ChoiceField(choices=city_choice)
    Password = forms.CharField(widget=forms.PasswordInput())
    Password_confirm = forms.CharField(widget=forms.PasswordInput())


class UpdateForm(forms.ModelForm):
    city_choice = [
        ("Dnipro", "Dnipro"),
        ("Kyiv", "Kyiv"),
        ("Kharkiv", "Kharkiv"),
        ("Odesa", "Odesa"),
        ("Lviv", "Lviv"),
        ("Zaporizhzhia", "Zaporizhzhia"),
        ("Kryvyi Rih", "Kryvyi Rih"),
        ("Mykolaiv", "Mykolaiv"),
        ("Mariupol", "Mariupol"),
        ("Luhansk", "Luhansk"),
        ("Vinnytsia", "Vinnytsia"),
        ("Kherson", "Kherson"),
        ("Poltava", "Poltava"),
        ("Chernihiv", "Chernihiv"),
        ("Cherkasy", "Cherkasy"),
        ("Sumy", "Sumy"),
        ("Zhytomyr", "Zhytomyr"),
        ("Ivano-Frankivsk", "Ivano-Frankivsk"),
        ("Ternopil", "Ternopil"),
        ("Chernivtsi", "Chernivtsi"),
        ("Rivne", "Rivne"),
        ("Kropyvnytskyi", "Kropyvnytskyi"),
        ("Khmelnytskyi", "Khmelnytskyi"),
        ("Uzhhorod", "Uzhhorod")
    ]
    gender_choice = [('M', 'Male'), ('F', 'Female'),]

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    Gender = forms.ChoiceField(choices=gender_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    Phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Country = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    City = forms.ChoiceField(choices=city_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    Password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    Avatar = forms.ImageField(
        required=False,
        label='Profile Picture',
        help_text='Upload a profile picture.',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )


# class ProfileForm(ModelForm):
#     class Meta:
#         model = ProfileImage
#         fields = ['profile_image', 'description']





