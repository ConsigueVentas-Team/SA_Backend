from api.model.ScheduleModel import Schedule

schedulesMorning = [
    {"dayOfWeek": 1, "startTime": "08:00", "endTime": "13:00"},
    {"dayOfWeek": 1, "startTime": "08:00", "endTime": "13:00"}, 
    {"dayOfWeek": 2, "startTime": "08:00", "endTime": "13:00"},
    {"dayOfWeek": 3, "startTime": "08:00", "endTime": "13:00"},
    {"dayOfWeek": 4, "startTime": "08:00", "endTime": "13:00"},
    {"dayOfWeek": 5, "startTime": "08:00", "endTime": "13:00"},
]

schedulesAfternoon = [
    {"dayOfWeek": 1, "startTime": "14:30", "endTime": "19:00"},
    {"dayOfWeek": 1, "startTime": "14:30", "endTime": "19:00"}, 
    {"dayOfWeek": 2, "startTime": "14:30", "endTime": "19:00"},
    {"dayOfWeek": 3, "startTime": "14:30", "endTime": "19:00"},
    {"dayOfWeek": 4, "startTime": "14:30", "endTime": "19:00"},
    {"dayOfWeek": 5, "startTime": "14:30", "endTime": "19:00"},
]

def createSchedulesMorning(user_id):
    # Crear horarios de lunes a viernes de 8:00 am a 1:00 pm
    for schedule_data in schedulesMorning:
        Schedule.objects.create(
            dayOfWeek=schedule_data['dayOfWeek'],
            startTime=schedule_data['startTime'],
            endTime=schedule_data['endTime'],
            user_id=user_id
        )

def createSchedulesAfternoon(user_id):
    # Crear horarios de lunes a viernes de 2:30 pm a 7:00 pm
    for schedule_data in schedulesAfternoon:
        Schedule.objects.create(
            dayOfWeek=schedule_data['dayOfWeek'],
            startTime=schedule_data['startTime'],
            endTime=schedule_data['endTime'],
            user_id=user_id
        )
