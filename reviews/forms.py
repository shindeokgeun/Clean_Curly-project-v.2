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

from django import forms

class ReportForm(forms.Form):
    REPORT_REASONS = [
        ('spam', '도배성 게시물'),
        ('offensive', '비방 및 욕설'),
        ('inappropriate', '부적절한 내용'),
        ('false_info', '허위 정보'),
        ('copyright', '저작권 침해'),
        ('other', '기타'),
    ]
    reason = forms.ChoiceField(choices=REPORT_REASONS, widget=forms.RadioSelect, label='신고 사유')
    other_reason = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': '최소 10글자, 최대 100글자로 입력해주세요.'}),
        required=False,
        min_length=10,
        max_length=100,
        label='기타 사유'
    )
    block_user = forms.BooleanField(required=False, label='해당 게시물을 차단합니다.')

    def clean(self):
        cleaned_data = super().clean()
        reason = cleaned_data.get('reason')
        other_reason = cleaned_data.get('other_reason')

        if reason == 'other':
            if not other_reason:
                raise forms.ValidationError("'기타' 선택 시 상세 사유를 입력해주세요.")
            if len(other_reason) < 10 or len(other_reason) > 100:
                raise forms.ValidationError("기타 사유는 10글자 이상 100글자 이하로 입력해주세요.")

        return cleaned_data