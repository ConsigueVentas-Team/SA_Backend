def getRol(rol):
        if rol == 1:
            return {'id': 1, 'name': 'Gerencia'}
        elif rol == 2:
            return {'id': 2, 'name': 'Lider Nucleo'}
        elif rol == 3:
            return {'id': 3, 'name': 'Colaborador'}
        elif rol == 4:
            return {'id': 4, 'name': 'Lider Departamento'}
        else:
            return {'id': 0, 'name': 'Rol no válido'}