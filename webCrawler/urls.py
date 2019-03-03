from django.urls import path
from . import views


app_name = 'baseApp'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homePage'),
    path('crawler/crawl/', views.HomePageView.as_view(), name='crawler')
]
