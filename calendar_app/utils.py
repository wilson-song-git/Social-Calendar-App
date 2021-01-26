# calendarapp/utils.py

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event  , Group


class Calendar(HTMLCalendar ):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day

	def formatday(self, day, events  , group):
		if group is None:
			events_per_day = events.filter(date__day=day , group=None )
		else:
			events_per_day = events.filter(date__day=day , group= group )

		d = ''
		event_greter = Event.objects.none().first()
		max_value = 0
		for event in events_per_day:
			if event.priority.scale > max_value:
				max_value , event_greter  = event.priority.scale , event
		try:

			if group  is None:
				d += f"""
				<li class="list-group-item"> {event_greter.get_html_url} </li>
				{event_greter.get_all_events}  
				"""
			else:
				d += f"""
				<li class="list-group-item"> {event_greter.get_html_url} </li>
				{event_greter.get_all_events_by_group}  
				"""
		except:
			pass

		# 
		if day != 0:
		
			return f"""<td><span class='date'>
		  <a href="#eventmodel" data-toggle="modal"  > {day}</a>
			</span>
			<ul class="list-group custom"> {d} </ul>  
			
			</td>"""
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events  , group ):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events , group = group  )
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self,  user= None , group = None,  withyear=True):
		if user is not None:
			events = Event.objects.filter(date__year=self.year, date__month=self.month , user=user , group=None )
		else:
			events = Event.objects.filter(group =group , date__year=self.year, date__month=self.month )
		cal = f'<table  class="calendar" style="width:100%" >\n'
		# cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()} \n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events , group = group  )} \n'
		return cal