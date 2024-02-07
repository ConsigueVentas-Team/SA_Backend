from rest_framework.response import Response
from rest_framework import generics, status, permissions
from api.model.AttendanceModel import Attendance
from api.model.ScheduleModel import Schedule
from api.model.JustificationModel import Justification
from api.serializers.AttendanceSerializer import AttendanceSerializer
from datetime import datetime, time
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from datetime import datetime, time

class AttendanceList(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = Attendance.objects.all()
            
            #Recogemos los valores de los parametros para filtrado
            date = self.request.query_params.get('date', None)
            core = self.request.query_params.get('core', None)
            department = self.request.query_params.get('department', None)
            shift = self.request.query_params.get('shift', None)

            #Validamos que los parametros existan, en ese caso procedemos al filtrado
            if date:
                queryset = queryset.filter(date=date)
            if core:
                queryset = queryset.filter(user__position__core__name=core)
            if department:
                queryset = queryset.filter(user__position__core__department__name=department)
            if shift:
                queryset = queryset.filter(user__shift=shift)
            
            #Retornamos el resultado
            return queryset
        except Exception as e:
            # Manejar cualquier excepción y registrarla si es necesario
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AttendanceByID(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            user_id = self.request.user.id
            queryset = Attendance.objects.filter(user__id=user_id)
            return queryset
        except Exception as e:
            # Manejar cualquier excepción y registrarla si es necesario
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AttendanceCreateAPIView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def is_late_for_check_in(self, admission_time_str, start_time):
        # Convertir las cadenas de texto a objetos de tipo datetime.time
        admission_time = datetime.strptime(admission_time_str, '%H:%M:%S').time()
        return admission_time > start_time

    def upload_image(self, image):
        try:
            # Subir imagen al servidor
            folder_name = datetime.now().strftime('%Y-%m-%d')
            path = f"attendances/{folder_name}"
            filename = f"{int(time())}-{image.name}"
            image_path = default_storage.save(f"{path}/{filename}", ContentFile(image.read()))
            return image_path
        except Exception as e:
            raise Exception('Error al subir la imagen.')

    def has_justification(self, user):
        try:
            flag = 2
            today = datetime.now().date()
            justification_exists = Justification.objects.filter(user=user, justification_date=today).first()
            if justification_exists is None:
                return flag
            else:
                return justification_exists.type  # 0 | 1
        except Exception as e:
            raise Exception('Error al verificar la justificación.')

    def post(self, request, *args, **kwargs):
        try:
            #Asignacion de datos
            auth_user_id = request.user.id
            current_time = datetime.now()
            today = datetime.now().date()
            
            #Buscamos la asistencia de hoy
            attendance = Attendance.objects.filter(user_id=auth_user_id, date=today).first()

            #Validamos si existe la asistencia de hoy
            if attendance.attendance == 0 and attendance.delay == 0:
                #Marcado de entrada
                self.update_check_in(attendance, current_time, request.data.get('admission_image'), auth_user_id)
            else:
                #Marcado de salida
                self.update_check_out(attendance, current_time, request.data.get('departure_image'))

            #Validacion del serializador
            serializer = self.get_serializer(attendance)
            #Retornamos los valores
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_check_in(self, attendance, current_time, image_path, auth_user_id):
        #try:
            # Formateo para día de la semana
            day_of_week = current_time.weekday()
            
            print("Auth User:", auth_user_id)
            print("Day Of week:", day_of_week)

            # Obtener el horario personalizado para el usuario logueado
            schedule_user = Schedule.objects.filter(user=auth_user_id, dayOfWeek=day_of_week).get()
            
            print("Schedule:", schedule_user)
            
            #Si exsite el horario, procedemos a marcar la entrada
            if schedule_user:
                # Asignacion de parametros
                admission_time = current_time.strftime("%H:%M:%S")
                #admission_image = self.upload_image(image_path)
                
                admission_image = "image.png"
                print("Admission Time:",admission_time)
                
                # Actualizar los datos de asistencia
                attendance.admissionTime = admission_time
                attendance.admissionImage = admission_image
                attendance.user_id = auth_user_id
                attendance.date = current_time.date()

                # Verificar si el usuario llegó tarde según el horario personalizado
                delay = self.is_late_for_check_in(admission_time, schedule_user.startTime)
                print("Justification:", delay)
                
                if delay:
                    # El usuario llegó tarde, verificamos si tiene justificacion
                    justification_type = self.has_justification(auth_user_id)
                    #No tiene justificacion, marcamos tardanza
                    if justification_type == 2:
                        attendance.delay = 1
                    #Tiene justificacion, marcamos tardanza pero justificada
                    else:
                        attendance.justification = 1
                        attendance.delay = 1
                else:
                    # El usuario llegó a tiempo
                    attendance.attendance = 1
                attendance.save()
            else:
                raise Exception('No existe un horario para el usuario elegido')
        #except Exception as e:
        #    raise Exception('Error al actualizar el check-in.')

    def update_check_out(self, attendance, current_time, image_path):
        try:
            departure_time = current_time.strftime('%H:%M')
            #departure_image = self.upload_image(image_path)
            departure_image = "image.png"
            attendance.departureTime = departure_time
            attendance.departureImage = departure_image
            attendance.save()
        except Exception as e:
            raise Exception('Error al actualizar el check-out.')

class AttendanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer