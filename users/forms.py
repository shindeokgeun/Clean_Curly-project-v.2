from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction 

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'login__input',
            'placeholder': '전화번호를 입력해주세요',
            'id': 'phone_number',
        }),
        label='전화번호'
    )

    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'login__input',
            'placeholder': '주소를 입력해주세요',
            'id': 'address',
        }),
        label='주소'
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'login__input',
            'placeholder': '연도-월-일 형식으로 생년월일을 입력해주세요',
            'id': 'date_of_birth',
            'type': 'date',
        }),
        label='생년월일'
    )

    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        required=False,
        label='프로필 사진'
    )


    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address', 'date_of_birth', 'profile_picture')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'login__input',
            'placeholder': '아이디를 입력해주세요',
            'id': 'username',
            'aria-invalid': 'false',
            'aria-describedby': 'usernameError',
        }),
        label='아이디'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login__input',
            'placeholder': '비밀번호를 입력해주세요',
            'id': 'password',
            'aria-invalid': 'false',
            'aria-describedby': 'passwordError',
        }),
        label='비밀번호'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'is_active', 'is_staff', 'is_superuser')

from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='이메일')
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label='새 비밀번호')  # 비밀번호 필드
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='새 비밀번호 확인')  # 확인 비밀번호

    class Meta:
        model = CustomUser
        fields = ['email','phone_number', 'address', 'date_of_birth', 'profile_picture', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise ValidationError('새 비밀번호와 확인 비밀번호가 일치하지 않습니다.')

        return cleaned_data


class MileageUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['mileage', 'karly_cash']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mileage'].label = '적립금 추가'
        self.fields['karly_cash'].label = '칼리캐시 추가'


