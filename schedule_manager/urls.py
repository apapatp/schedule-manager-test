from django.urls import path
from rest_framework import routers
from schedule_manager.auth.views import (
    LoginView,
    LogoutView,
    RegisterView,
    TokenRefreshView
)
from schedule_manager.views import (
    ScheduleViews
)

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'schedule', ScheduleViews, basename='schedule')

urlpatterns = [
    path("login", LoginView.as_view(), name="login-user"),
    path("logout", LogoutView.as_view(), name="logout-user"),
    path("register", RegisterView.as_view(), name="register-user"),
    path("refresh/token", TokenRefreshView.as_view(), name="refresh-token"),

]

urlpatterns += router.urls
