def target_move(game, target):
    # ... other moves

    if target.current_location == target.destination_location:
        target.has_reached_destination = True


def calculate_target_reward(game, target):
    if target.has_reached_destination:
        return target.cocaine_weight_in_kilograms

    return 0
