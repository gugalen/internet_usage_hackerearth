from django.db.models import Sum
from django.http.response import JsonResponse
from internet.models import UsageData
from internet.serializers import DataSerializer
from django.utils import timezone
from datetime import timedelta, datetime
import datetime
from django.db import connection


def dataApi(request):
    dataset = UsageData.objects.all()
    data_serializer = DataSerializer(dataset, many=True)
    return JsonResponse(data_serializer.data, safe=False)


def userApi(request):
    try:
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'ok': False, 'error': {'message': 'Please provide valid username'}}, status=422)

        user = UsageData.objects.filter(username=username)

        if len(user) == 0:
            return JsonResponse({'ok': False, 'error': {'message': 'user not found'}}, status=400)

        last_hour_usage = UsageData.objects.filter(username=username,
                                                   start_time__gte=timezone.now() - timedelta(hours=1)) \
            .values('username').annotate(upload=Sum("upload"), download=Sum("download"), time=Sum("usage_time"))
        last_six_hours_usage = UsageData.objects.filter(username=username,
                                                        start_time__gte=timezone.now() - timedelta(hours=6)) \
            .values('username').annotate(upload=Sum("upload"), download=Sum("download"), time=Sum("usage_time"))
        last_twenty_four_hours_usage = UsageData.objects.filter(username=username,
                                                                start_time__gte=timezone.now() - timedelta(hours=24)) \
            .values('username').annotate(upload=Sum("upload"), download=Sum("download"), time=Sum("usage_time"))
        combined_usage = last_hour_usage.union(last_six_hours_usage, last_twenty_four_hours_usage)

        usage = combined_usage.values('username', 'time', 'upload', 'download')
        new_usage = []
        for u in usage:
            nu = {k: v for k, v in u.items() if k != 'username'}
            new_usage.append(nu)

        for u in new_usage:
            for k, v in u.items():
                if k == 'time':
                    duration_str = u[k]
                    hours, remainder = divmod(duration_str.total_seconds(), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    formatted_duration = f"{int(hours)}h{int(minutes)}m"
                    u[k] = formatted_duration
                elif k in ['upload', 'download']:
                    x = float(v / 1024 / 1024 / 1024)
                    u[k] = f'{x:.1f} GB'
                    if float(x) < 1:
                        x = float(v / 1024 / 1024)
                        u[k] = f'{x:.1f} MB'

        res = {"ok": True,
               "data": {
                   "username": username,
                   "lastHourUsage": new_usage[2] if new_usage else 0,
                   "last6HourUsage": new_usage[1] if new_usage else 0,
                   "last24HourUsage": new_usage[0] if new_usage else 0
               }}
        return JsonResponse(res, safe=False)

    except Exception as e:
        return JsonResponse({'ok': False, 'error': {'message': e}}, status=500)


def top_users_by_internet_usage(request):
    try:
        date = request.GET.get('date')
        if date is None:
            new_date = timezone.now()
        else:
            new_date = datetime.datetime.strptime(date, "%d%m%Y")
            # TODO: if date format is incorrect handle it
            now = datetime.datetime.now()
            if new_date > now:
                return JsonResponse({'ok': False, 'error': {'message': 'Invalid date'}}, status=400)

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))

        sql_query = f'''
        SELECT username,
        SUM(CASE WHEN start_time <= '{new_date}'::timestamp and start_time >= ('{new_date}'::timestamp - interval '1 day') THEN usage_time END) as usage_time_1day,
        SUM(CASE WHEN start_time <= '{new_date}'::timestamp and start_time >= ('{new_date}'::timestamp - interval '7 days') THEN usage_time END) as usage_time_7days,
        SUM(CASE WHEN start_time <= '{new_date}'::timestamp and start_time >= ('{new_date}'::timestamp - interval '30 days') THEN usage_time END) as usage_time_30days
        FROM internet_usagedata
        GROUP BY username
        ORDER BY usage_time_30days DESC NULLS LAST limit {limit} offset {limit * (page - 1)};
        '''

        cursor = connection.cursor()
        cursor.execute(sql_query)
        res = cursor.fetchall()

        all_empty = True

        for r in res:
            if not (r[1] is None and r[2] is None and r[3] is None):
                all_empty = False
                break

        if all_empty:
            return JsonResponse({'ok': True, 'data': []}, status=422)

        new_res = []
        for r in res:
            dict = {}
            dict["username"] = r[0]
            if r[1]:
                one_day_duration_str = r[1]
                one_day_hours, remainder = divmod(one_day_duration_str.total_seconds(), 3600)
                one_day_minutes, seconds = divmod(remainder, 60)
                one_day_formatted_duration = f"{int(one_day_hours)}h{int(one_day_minutes)}m"
                dict["lastDayUsage"] = one_day_formatted_duration

            if r[2]:
                seven_day_duration_str = r[2]
                seven_day_hours, remainder = divmod(seven_day_duration_str.total_seconds(), 3600)
                seven_day_minutes, seconds = divmod(remainder, 60)
                seven_day_formatted_duration = f"{int(seven_day_hours)}h{int(seven_day_minutes)}m"
                dict["sevenDayUsage"] = seven_day_formatted_duration

            if r[3]:
                thirty_day_duration_str = r[3]
                thirty_day_hours, remainder = divmod(thirty_day_duration_str.total_seconds(), 3600)
                thirty_day_minutes, seconds = divmod(remainder, 60)
                thirty_day_formatted_duration = f"{int(thirty_day_hours)}h{int(thirty_day_minutes)}m"
                dict["thirtyDayUsage"] = thirty_day_formatted_duration
            new_res.append(dict)

        sql_count_query = f'''
                SELECT 
                SUM(CASE WHEN start_time <= '{new_date}'::timestamp and start_time >= ('{new_date}'::timestamp - interval '1 day') THEN usage_time END) as usage_time_1day,
                SUM(CASE WHEN start_time <= '{new_date}'::timestamp and start_time >= ('{new_date}'::timestamp - interval '7 days') THEN usage_time END) as usage_time_7days,
                SUM(CASE WHEN start_time <= '{new_date}'::timestamp and start_time >= ('{new_date}'::timestamp - interval '30 days') THEN usage_time END) as usage_time_30days
                FROM internet_usagedata
                GROUP BY username;
                '''

        cursor = connection.cursor()
        cursor.execute(sql_count_query)
        count_res = cursor.fetchall()
        total_recs = len(count_res)

        total_pages = 1 if total_recs <= limit else round(total_recs / limit)

        if page > total_pages:
            return JsonResponse({'ok': True, 'data': []}, status=422)

        final_res = {
            "ok": True,
            "data": [] if len(res) == 0 else new_res,
            "page": page,
            "pageSize": limit,
            "totalPages": total_pages
        }
        return JsonResponse(final_res, safe=False)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': {'message': e}}, status=500)
