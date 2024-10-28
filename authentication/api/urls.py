from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    GetWorkSites, UserAPIView, 
    Login, GetMyUserDetail, LogOutUser, UpdatePassword, GetMyWorkSiteRole,
    GetMyDepartments,
    GetSubContractors, GetWitnesses, GetCorrectiveActionUsers, GetQualityEngineers, GetExecutionEngineers
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", LogOutUser.as_view(), name="logout"),
    # Token logout is not implemented
    path("update-password/", UpdatePassword.as_view(), name="update_password"),

    path('user/', UserAPIView.as_view()),
    path('work-sites/', GetWorkSites.as_view()),

    path("my-departments/", GetMyDepartments.as_view(), name="my_departments"),

    path("my-detail/", GetMyUserDetail.as_view(), name="my_user_detail"),
    path("my-work-site-role/", GetMyWorkSiteRole.as_view(), name="my_work_site_role"),
    
    path("user/sub-contractor/", GetSubContractors.as_view(), name="get_sub_contractors"),
    path("user/witness/", GetWitnesses.as_view(), name="get_witnesses"),
    path("user/quality-engineer/", GetQualityEngineers.as_view(), name="get_quality_engineers"),
    path("user/execution-engineer/", GetExecutionEngineers.as_view(), name="get_execution_engineers"),
    path("user/corrective-action-user/", GetCorrectiveActionUsers.as_view(), name="get_corrective_action_users"),
]
