class Config:
    TEST_MODE = True
    BATCH_SIZE = 64
    BUFFER_SIZE = 1000
    OUTPUT_CLASSES = 24
    EPOCHS = 75
    VAL_SUBSPLITS = 5
    VALIDATION_STEPS = 2
    STEPS_PER_EPOCH = 7

    WEIGHTS = "/src/model/weights/modelv2_run_4_weights.weights.h5"

    label_to_name = {
        1: "diamond_warning_sign",
        2: "diamond_warning_sign_back",
        3: "speed_limit_sign",
        4: "speed_limit_sign_back",
        5: "stop_sign",
        6: "stop_sign_back",
        7: "small_informational_sign",
        8: "small_informational_sign_back",
        9: "large_informational_sign",
        10: "large_informational_sign_back",
        11: "yield_sign",
        12: "yield_sign_back",
        13: "freeway_sign",
        14: "freeway_sign_back",
        15: "traffic_cone",
        16: "mile_marker",
        17: "mile_marker_back",
        18: "road_work_sign",
        19: "road_work_sign_back",
        20: "tourist_help_sign",
        21: "tourist_help_sign_back",
        22: "info_sign",
        23: "info_sign_back"
    }