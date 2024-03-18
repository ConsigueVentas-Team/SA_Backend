from datetime import datetime
from api.model.UserModel import User
from api.model.AttendanceModel import Attendance
from api.model.JustificationModel import Justification
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from api.CustomPagination import CustomPageNumberPagination

class ReportListAPIView(ListAPIView):
    serializer_class = None  # Define tu serializador aquí
    pagination_class = CustomPageNumberPagination
    
    def list(self, request, *args, **kwargs):
        # Obtener los totales de asistencias, faltas, tardanzas y justificaciones de hoy
        total_asistencias = Attendance.objects.filter(date__month=datetime.now().month, date__year=datetime.now().year).count()
        total_faltas = Attendance.objects.filter(date__month=datetime.now().month, date__year=datetime.now().year, justification=False).count()
        total_tardanzas = Attendance.objects.filter(date__month=datetime.now().month, date__year=datetime.now().year, delay=True).count()
        total_justificaciones = Justification.objects.count()

        # Obtener el total de usuarios activos e ingresos del mes
        total_users = User.objects.count()
        usuarios_activos = User.objects.filter(status=True).count()
        ingresos_mes = User.objects.filter(created_at__month=datetime.now().month, created_at__year=datetime.now().year).count()

        # Obtener el total de justificaciones aceptadas, en proceso y rechazadas
        total_justification_aceptado = Justification.objects.filter(justification_status=1).count()
        total_justification_en_proceso = Justification.objects.filter(justification_status=3).count()
        total_justification_rechazado = Justification.objects.filter(justification_status=2).count()

        # Crear el objeto JSON de respuesta
        data = {
            "reportes_asistencias": [
                {
                    "department_attendance_count": total_asistencias,
                    "department_absence_count": total_faltas,
                    "department_delay_count": total_tardanzas,
                    "department_justification_count": total_justificaciones
                }
            ],
            "reportes_usuarios": {
                "reporte_general": [],  # Aquí puedes incluir datos específicos de usuarios si lo necesitas
                "reporte_total": {
                    "total_usuarios": total_users,
                    "usuarios_activos": usuarios_activos,
                    "ingresos_mes": {"count": ingresos_mes}
                }
            },
            "reportes_justificacion": {
                "total_justification_aceptado": total_justification_aceptado,
                "total_justification_en_proceso": total_justification_en_proceso,
                "total_justification_rechazado": total_justification_rechazado,
                "total_justifications": total_justificaciones,
            }
        }

        return Response({"data": data, "count": 1})
