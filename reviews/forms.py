from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (5, '아주 좋아요'),
        (4, '좋아요'),
        (3, '보통이에요'),
        (2, '그냥 그래요'),
        (1, '별로에요'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'review__rating-radio'}),
        label='평점'
    )
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = Review
        fields = ['rating', 'text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': '리뷰를 남겨주세요. (최소 10자 이상)',
                'class': 'review__textarea',
                'rows': 4,
                'minlength': '10',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'review__image-input',
                'accept': 'image/*'
            })
        }
        labels = {
            'text': '리뷰 내용',
            'image': '리뷰 이미지'
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        return int(rating)

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise forms.ValidationError("리뷰는 최소 10자 이상 작성해주세요.")
        return text

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5*1024*1024:  # 5MB
                raise forms.ValidationError("이미지 크기는 5MB를 초과할 수 없습니다.")
        return image