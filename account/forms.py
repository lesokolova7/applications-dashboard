# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
#
#
# class CustomUserCreationForm(UserCreationForm):
#     password1 = forms.CharField(
#         label="Пароль",
#         widget=forms.PasswordInput,
#         help_text="Ваш пароль должен содержать не менее 8 символов.\n"
#         "Ваш пароль не может состоять только из строк или чисел.",
#     )
#     password2 = forms.CharField(
#         label="Подтверждение пароля",
#         widget=forms.PasswordInput,
#         help_text="Введите тот же пароль для подтверждения.",
#     )
#
#     class Meta:
#         model = User
#         fields = ["username", "password1", "password2"]
#         labels = {
#             "username": "Имя пользователя",
#         }
#         help_texts = {
#             "username": "не более 150 символов. Только буквы, цифры и @/./+/-/_."
#         }
#         error_messages = {
#             "username": {
#                 "required": "Имя пользователя обязательно.",
#                 "unique": "Имя пользователя уже занято.",
#             },
#             "password1": {
#                 "required": "Пароль обязателен.",
#             },
#             "password2": {
#                 "required": "Подтверждение пароля обязательно.",
#                 "password_mismatch": "Пароли не совпадают.",
#             },
#         }
