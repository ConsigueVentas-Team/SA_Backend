from enum import Enum

class RoleEnum(Enum):
    MANAGEMENT = 1
    TEAM_LEADER = 2
    COLLABORATOR = 3

class JustificationStatus(Enum):
  ACEPTADO = 1
  RECHAZADO = 2
  EN_PROCESO = 3