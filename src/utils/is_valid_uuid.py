from uuid import UUID

def is_valid_uuid(possible_uuid):

    try:
        UUID(possible_uuid)
        return True

    except ValueError:
        return False