from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser

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
        required=False,  # Optional, depending on whether you want to make this field required
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
