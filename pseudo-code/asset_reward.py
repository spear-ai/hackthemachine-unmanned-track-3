def asset_move(game, asset):
    for sensor in asset.sensor_list:
        # Assume EO/IR detections are positive identifications
        if sensor.type == 'eo' or sensor.type == 'ir':
            for detection in sensor.ping():
                # Assume a detection is accurate
                game.total_positive_identifications += 1


def calculate_asset_reward(game):
    # Return a point for each target positively identified
    return 1 * game.total_positive_identifications
