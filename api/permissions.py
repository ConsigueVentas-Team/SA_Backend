from rest_framework.permissions import BasePermission

#Pernmiso de Gerencia 
class IsManagement(BasePermission):
    """
    Allows access only to manager users.
    """

    def has_permission(self, request, view):
        return bool(request.user.role == 1)

#Pernmiso de Lider Nucleo 
class IsTeamLeader(BasePermission):
    """
    Allows access only to Team leader users.
    """

    def has_permission(self, request, view):
        return bool(request.user.role == 2)


#Pernmiso de Colaborador 
class IsCollaborator(BasePermission):
    """
    Allows access only to collaborator users.
    """

    def has_permission(self, request, view):
        return bool(request.user.role == 3)
    
#Pernmiso de Lider Departamento 
class IsTeamLeader(BasePermission):
    """
    Allows access only to Team leader users.
    """

    def has_permission(self, request, view):
        return bool(request.user.role == 4)