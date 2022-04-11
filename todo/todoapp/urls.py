from django.urls import path
from todoapp import views


urlpatterns=[
    path("todos",views.TodoMixinList.as_view()),
    path("todos/<int:id>",views.TodoMixinDetails.as_view()),
    path("todos/accounts/signup",views.UserCreateMixin.as_view()),
    path("todos/accounts/signin",views.SigninView.as_view())
    ]