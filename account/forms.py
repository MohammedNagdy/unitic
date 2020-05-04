from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


SECTORS = [
        ("aviation"," صناعة الطيران"),
        ("transport"," صناعة النقل"),
        ("computer"," صناعة الكمبيوتر"),
        ("telecommunication"," صناعة الاتصالات"),
        ("agriculture"," صناعة الزراعة"),
        ("construction"," صناعة البناء والتشييد"),
        ("education"," صناعة التعليم"),
        ("pharmaceutical"," الصناعة الدوائية"),
        ("food"," صناعة المواد الغذائية"),
        ("health_care"," صناعة الرعاية الصحية"),
        ("hospitality"," صناعة الضيافة"),
        ("entertainment"," صناعة الترفيه"),
        ("news_media"," صناعة الأخبار الإخبارية"),
        ("energy"," صناعة الطاقة"),
        ("manufacturing"," الصناعة التحويلية"),
        ("music"," صناعة الموسيقى"),
        ("mining"," صناعة التعدين"),
        ("worldwide_web"," الشبكة العالمية"),
        ("electronics"," صناعة الإلكترونيات"),

]


# add other fields for users
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, )
    email = forms.EmailField()
    phone_num = forms.CharField(max_length=20)


    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'phone_num',

        ]
