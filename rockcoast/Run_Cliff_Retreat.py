from matplotlib import pyplot as plt
from Model import RockCoast
import json
with open('config.json', 'r') as f:
    config = json.load(f)

CR = RockCoast()
CR.SeaLevelRise=config['SeaLevelRise']
CR.EarthquakeTime =config['EarthquakeTime']
CR.EarthquakeUplift = config['EarthquakeUplift']
CR.InitialSlope = config['InitialSlope']

CR.WaveHeight = config['WAVEHEIGHT']
CR.WaveForceCoef = config['WaveForceCoef']
CR.WaveDecayCoef = config['DECAY_COEFFICIENT']
CR.TidalRange = config['TIDAL_RANGE']

CR.MaxResistance = config['MAX_RESISTANCE']
CR.MaxWeatheringEfficacy = config['MAX_WEATHERING_EFFICIENT']
CR.RunModel()
plt.show()