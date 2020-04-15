def get_start_and_end_time(event):
    start_time = event["start"]["dateTime"].split("T")
    start_time = start_time[1].split("+")
    start_time = start_time[0].split(":")
    start_time = start_time[0] + ":" + start_time[1]
    end_time = event["end"]["dateTime"].split("T")
    end_time = end_time[1].split("+")
    end_time = end_time[0].split(":")
    end_time = end_time[0] + ":" + end_time[1]
    return [start_time, end_time]


def get_next_event(service, temp_now, next=0):
    events_list = []
    if 0 <= next <= 3:
        if next == 0:
            time_min = temp_now.isoformat() + 'Z'
            time_max = temp_now.replace(month=((temp_now.month + 1) % 12)).isoformat() + 'Z'
        elif next == 1:
            time_min = temp_now.isoformat() + 'Z'
            time_max = temp_now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        elif next == 2:
            try:
                time_min = temp_now.replace(day=temp_now.day + 1, hour=0, minute=0, second=0).isoformat() + 'Z'
                time_max = temp_now.replace(day=temp_now.day + 1, hour=23, minute=59, second=59).isoformat() + 'Z'
            except ValueError:
                time_min = temp_now.replace(day=1, hour=0, minute=0, second=0).isoformat() + 'Z'
                time_max = temp_now.replace(day=1, hour=23, minute=59, second=59).isoformat() + 'Z'
        events = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            maxResults=10
        ).execute()
        for event in events['items']:
            events_list.append(event)
    next_event = None
    if len(events_list) > 0:
        next_event = events_list[0]
    time = ""
    if next == 1:
        time = "today "
    elif next == 2:
        time = "tomorrow "
    if next_event is not None:
        end_and_start = get_start_and_end_time(next_event)
        return "Your next event " + time + " called " + next_event["summary"] + " starts at " + end_and_start[
            0] + " and ends at " + end_and_start[1]
    else:
        return "You don't have any more event " + time


def get_last_event(service, temp_now, today=True):
    if today:
        time_min = temp_now.isoformat() + 'Z'
        time_max = temp_now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
    else:
        try:
            time_min = temp_now.replace(day=temp_now.day + 1, hour=0, minute=0, second=0).isoformat() + 'Z'
            time_max = temp_now.replace(day=temp_now.day + 1, hour=23, minute=59, second=59).isoformat() + 'Z'
        except ValueError:
            time_min = temp_now.replace(day=1, hour=0, minute=0, second=0).isoformat() + 'Z'
            time_max = temp_now.replace(day=1, hour=23, minute=59, second=59).isoformat() + 'Z'
    page_token = None
    events_list = []
    while True:
        events = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            maxResults=10
        ).execute()
        for event in events['items']:
            events_list.append(event)
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    last_event = None
    time = "today" if today else "tomorrow"
    if len(events_list) > 0:
        last_event = events_list[-1]
    if last_event is not None:
        end_and_start = get_start_and_end_time(last_event)
        return "Your last event " + time + " called " + last_event["summary"] + " starts at " + \
               end_and_start[0] + " and ends at " + end_and_start[1]
    else:
        return "You don't have anymore events " + time


def get_all_day_events(service, temp_now, today=True):
    if today:
        time_min = temp_now.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        time_max = temp_now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
    else:
        try:
            time_min = temp_now.replace(day=temp_now.day + 1, hour=0, minute=0, second=0).isoformat() + 'Z'
            time_max = temp_now.replace(day=temp_now.day + 1, hour=23, minute=59, second=59).isoformat() + 'Z'
        except ValueError:
            time_min = temp_now.replace(day=1, hour=0, minute=0, second=0).isoformat() + 'Z'
            time_max = temp_now.replace(day=1, hour=23, minute=59, second=59).isoformat() + 'Z'
    page_token = None
    events_list = []
    while True:
        events = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            maxResults=10
        ).execute()
        for event in events['items']:
            events_list.append(event)
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    time = "today" if today else "tomorrow"
    if len(events_list) == 0:
        return "You don't have any event " + time
    else:
        all_events_string = ""
        for event in events_list:
            print(event)
            start_and_end = get_start_and_end_time(event)
            all_events_string += event["summary"] + " from " + start_and_end[0] + " to " + start_and_end[1] + ", "
        return "You have these following events " + time + ": " + all_events_string
