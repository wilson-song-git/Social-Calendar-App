# from sortedcontainers import SortedSet
import calendar
import datetime
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.views import View
from django.db.models import F
from .models import Event, Group, Priority
from .utils import Calendar


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class  MonthCalendar( LoginRequiredMixin, View):
    def get(self , request  , *args , **kwargs):
        date = get_date(request.GET.get('month', None))
        cal = Calendar(date.year, date.month)
        cal.setfirstweekday(6)
        user = request.user 

        # print('ye chala 2 ' , user)
        html_cal = cal.formatmonth(withyear=True , user = user)
        context ={}
        context['calendar'] = mark_safe(html_cal)
        context["date"] = date
        context['prev'] = prev_month(date)
        context['next'] = next_month(date)
        context['joined']=Group.objects.filter(user = request.user)
        return render(request , "calendar.html" ,context )
 

 
class CreateGroupView(LoginRequiredMixin , View):
    def post(self , request , *args , **kwargs):
        title = request.POST.get('grpname')
        title = slugify(title)
        if title:
            if Group.objects.filter(slug = title).first():
                print("ERRROR")
                messages.warning(request, "Group name is already taken  .")
                return redirect('calendar')
            else:
                group  = Group.objects.create(name =title  )
                group.user.add(request.user)
                messages.success(request, "group has been created .")
                return redirect('calendar')
        messages.warning(request, "Error. Group  not created .")
        return redirect('calendar')
        

class JoinGroupView( LoginRequiredMixin , View):
    def post(self , request , *args , **kwargs):
        id = request.POST.get('grpcode')
        group = Group.objects.filter(code = id).first()
        if group:
            group.user.add(request.user)
            messages.success(request, "group has been created .")
            return redirect('calendar')
        messages.warning(request, "Error. invalid Code ")
        return redirect('calendar')
         



class SwitchGroup(LoginRequiredMixin , View):
    def get(self , request  , *args , **kwargs):
        group_name= kwargs.get('group_name') 
        group  = Group.objects.filter(slug = group_name).first()
        date = get_date(request.GET.get('month', None))
        cal = Calendar(date.year, date.month)
        cal.setfirstweekday(6)
        html_cal = cal.formatmonth(withyear=True , group= group)
        context ={}
        context['calendar'] = mark_safe(html_cal)
        context["date"] = date
        context['prev'] = prev_month(date)
        context['next'] = next_month(date)
        context['group'] = group.slug
        context['joined']=Group.objects.filter(user = request.user)
        return render(request , "calendar.html" ,context )

 
class CreateEvent(LoginRequiredMixin , View):
    def post(self , request , *args , **kwargs):
        start_time         = request.POST.get('start_time')
        end_time           = request.POST.get('end_time')
        title              = request.POST.get('title')
        description        = request.POST.get('description')
        date               = request.POST.get('date')
        priority          = request.POST.get('priority')
        GROUP_REQUEST_SLUG = str(request.META.get('HTTP_REFERER'))
        group_slug         = GROUP_REQUEST_SLUG.split('/')[-2]
        group = Group.objects.filter(slug = group_slug).first()
        priority = Priority.objects.create(scale =priority )

        if Event.objects.filter(date=date):
            
            # print("same date")
            # start = start_time
            # end = end_time
            # r = range(start,end)
            # print('Hello world')
            # print(r)

            if Event.objects.filter(start_time__gte = start_time , end_time__lte=end_time):
               
                messages.success(request, "Event Overlapping .")     
                return redirect('calendar')
                # print("same time")
            else:
                print("time is different")
                if group is None:
                    Event.objects.create(date= date , title = title , start_time= start_time , end_time=end_time ,description= description , user= request.user , priority = priority)
                    messages.success(request, "Event has been createds .")
                else:
                    Event.objects.create(date= date , title = title , start_time= start_time , end_time=end_time ,description= description , user= request.user , group= group , priority = priority)

                    messages.success(request, f"Event has been created  in {group}")
                    return redirect('switch-group' ,group_slug )
                return redirect('calendar')
    
        
        else:
            print("Date is Not Same !")
            if group is None:
                Event.objects.create(date= date , title = title , start_time= start_time , end_time=end_time ,description= description , user= request.user , priority = priority)
                messages.success(request, "Event has been createds .")
            else:
                Event.objects.create(date= date , title = title , start_time= start_time , end_time=end_time ,description= description , user= request.user , group= group , priority = priority)

                messages.success(request, f"Event has been created  in {group}")
                return redirect('switch-group' ,group_slug )
            return redirect('calendar')


class EventDetailView(LoginRequiredMixin , View):
    def get(self , request , *args , **kwargs ):
        id = kwargs.get('event_id')
        event = Event.objects.get(id = id)
    
        context ={}
        context['event']=event 
        is_eligible  = self.request.user == event.user
        context['is_eligible']=is_eligible 
        return render(request , "event/eventdetail.html", context )
        
        
class EventDeleteView(LoginRequiredMixin , View):
    def get(self , request , *args , **kwargs):
        id = kwargs.get('event_id')
        e= Event.objects.get(id = id)
        e.delete()
        messages.warning(request, f"Event has been deleted successfuly ! ")
        return redirect('calendar')

from datetimerange import DateTimeRange


class DateEventAll(View):
    def get(self ,request,  *args , **kwargs):
        date = kwargs.get('date')
        evets  = Event.objects.filter(date=date).order_by('-created_date')
        context = {
            'date':date , 
            'events':evets 
        }
        return render(request , 'date/datedetail.html' ,  context)

class DateEventAllBygroup(View):
    def get(self ,request,  *args , **kwargs):
        date = kwargs.get('date')
        group = kwargs.get('group')
        print(date , group)
        group_ob = get_object_or_404(Group , name =group)


        evets  = Event.objects.filter(date=date , group=group_ob ).order_by('-created_date')
        context = {
            'date':date , 
            'events':evets 
        }
        return render(request , 'date/datedetail.html' ,  context)


        # list_of_pairs = []
        # temprange = DateTimeRange()
        # ordinary_Time=[]
        # priority_Time=[]
        # for evet in evets:
        #     print(evet , evet.start_time)
        #     start = datetime(evet.date.year , evet.date.month , evet.date.day , evet.start_time.hour ,evet.start_time.minute , evet.start_time.second )
        #     end = datetime(evet.date.year , evet.date.month , evet.date.day , evet.end_time.hour ,evet.end_time.minute , evet.end_time.second )
        #     rangeexample = DateTimeRange( start , end )
        #     list_of_pairs.append(rangeexample)
            
        # first  = list_of_pairs[0]
        # for some_range in list_of_pairs[:1]:
        #     tem3 = some_range.intersection(first)
        #     if tem3.NOT_A_TIME_STR == 'NaT':  # No overlap
        #         ordinary_Time.append(evet)
        #     else:
        #         priority_Time.append(evet )
        #     first = some_range
        # print(ordinary_Time )
        # print(priority_Time)





            # tem3 = rangeexample.intersection(temprange)
            # if tem3.NOT_A_TIME_STR == 'NaT':
            #     list_of_pairs.append(evet)
            # else:
            #     print("none")
            # temprange = rangeexample


            # print( evet.date , evet.start_time )
            # print(evet.date , evet.end_time)

            

    #     cutpoints = SortedSet()

    # for period in periods:
    #     cutpoints.add(period[1])
    #     cutpoints.add(period[2])

    # ranges = []

    # start_cutpoint = None
    # for end_cutpoint in cutpoints:

    #     if not start_cutpoint:  # skip first
    #         start_cutpoint = end_cutpoint
    #         continue

    #     cut_point_active_periods = []

    #     for period in periods:

    #         # check if period and cutpoint range overlap
    #         start_overlap = max(start_cutpoint, period[1])
    #         end_overlap = min(end_cutpoint, period[2])

    #         if start_overlap < end_overlap:
    #             cut_point_active_periods.append(period[0])

    #     ranges.append((cut_point_active_periods, start_cutpoint, end_cutpoint))
    #     start_cutpoint = end_cutpoint


# class EventUpdate(View):
#     def get(self , request , *args , **kwargs ): 
#         id = kwargs.get('event_id')
#         context ={}
#         context['event']= Event.objects.get(id = id)
#         return render(request , "event/update.html", context )

#     def post(self , request , *args , **kwargs):
#         id            = kwargs.get('event_id') 
#         e             = Event.objects.get(id = id)
#         e.title       = request.POST.get('title')
#         e.description = request.POST.get('description')
        
#         e.save()
#         return redirect('calendar')





class ProfileView(View):
    def get(self , request , *args , **kwargs):
        Groups = Group.objects.filter(user = request.user)
        return render(request , "profile.html" , {'groups':Groups})
