from django.urls import path

from spending.views import SignUpView,GetMeView
from spending.views import ExpenseListCreateView,ExpenseRetrieveUpdateDeleteView

from spending.views import ExpenseSummaryView
from spending.views import BudgetPlanView


from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns=[
    path('register/',SignUpView.as_view()),
    path('me/',GetMeView.as_view()),
    path('expenses/',ExpenseListCreateView.as_view()),
    path('expenses/<int:pk>/',ExpenseRetrieveUpdateDeleteView.as_view()),
    path('expenses/summary/',ExpenseSummaryView.as_view()),
    path('budgetplan/',BudgetPlanView.as_view()),

    path('token/',ObtainAuthToken.as_view()),
]