def getRol(rol):
        if rol == 1:
            return {'id': 1, 'name': 'Gerencia'}
        elif rol == 2:
            return {'id': 2, 'name': 'Líder Nucleo'}
        elif rol == 3:
            return {'id': 3, 'name': 'Colaborador'}
        else:
            return {'id': 0, 'name': 'Rol no válido'}