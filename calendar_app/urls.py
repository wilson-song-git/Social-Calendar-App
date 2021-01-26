from django.urls import path

from .views import (
    
    MonthCalendar ,
    CreateGroupView ,
    JoinGroupView ,
    SwitchGroup,
    CreateEvent , 
    EventDetailView  , 
    EventDeleteView , 
    ProfileView , 
    DateEventAll  , 
    DateEventAllBygroup

)

urlpatterns =[
    path('' , MonthCalendar.as_view() ,  name = 'calendar'),
    path('group/create/' , CreateGroupView.as_view() , name ='create-group'), 
    path('group/join/' , JoinGroupView.as_view() , name ='join-group'),
    path('group/<slug:group_name>/' , SwitchGroup.as_view() , name ='switch-group'), 
    path('event/create/' , CreateEvent.as_view() , name ='create-evetn'), 
    path('event/details/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('event/delete/<int:event_id>/', EventDeleteView.as_view(), name='event-delete'),
    path('event/profile/', ProfileView.as_view(), name='profile'),
    path('event/all/<str:date>/', DateEventAll.as_view(), name='event-all'),
    path('event/all/<str:date>/<str:group>/', DateEventAllBygroup.as_view(), name='event-all-group'),

]





















    # path('event/update/<int:event_id>/', EventUpdate.as_view(), name='event-update'),