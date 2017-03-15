from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
     available_permissions = {
        'create_short_course': True,
        'edit_short_course': True,
        'retrieve_any_student': True,
        'mark_payment': True,
        'list_all_students': True,
    }

class Estudent(AbstractUserRole):
     available_permissions = {
        'send_article': True,
    }
