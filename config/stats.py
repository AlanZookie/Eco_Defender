STATS_INITIAL = {
    "pollution": 0.10,      # 10%
    "deforestation": 0.20,  # 20%
}

STATS_RATES = {
    "pollution": 0.02,      
    "deforestation": 0.01, 
}

CLIMATE_WEIGHTS = {
    'Sunny': 0.6,
    'Rainy': 0.3,
    'Stormy': 0.1,
}

# How often (in seconds) to roll for a new climate
CLIMATE_CHANGE_INTERVAL = 20.0