from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
     available_permissions = {
        'create_short_course': True,
    }

class Estudent(AbstractUserRole):
     available_permissions = {
        'send_article': True,
    }
