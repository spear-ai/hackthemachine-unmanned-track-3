import create_vehicle


def create_force_package():
    # Assume each Seahawk is assigned to 1 Destroyer

    seahawk1 = create_vehicle({'id': 3})
    destroyer1 = create_vehicle({'id': 2})
    destroyer1.add_helicopter(seahawk1)

    seahawk2 = create_vehicle({'id': 3})
    destroyer2 = create_vehicle({'id': 2})
    destroyer2.add_helicopter(seahawk2)

    seahawk3 = create_vehicle({'id': 3})
    destroyer3 = create_vehicle({'id': 2})
    destroyer3.add_helicopter(seahawk3)

    return [destroyer1, destroyer2, destroyer3]
