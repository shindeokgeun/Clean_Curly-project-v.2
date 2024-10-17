from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

    def ready(self):
        # 커스텀 템플릿 태그 모듈을 임포트하여 등록
        import reviews.templatetags.review_extras
