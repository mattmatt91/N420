
from datetime import datetime, timedelta
from time import sleep, time
from log_data import Logger,Preferences
from gpiozero import CPUTemperature
from sensors import Sensor
import json as js
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)



class Growbox():
    actuators = []
    Sensor()
    cpu = CPUTemperature()
    data_logger = Logger('data')
    error_logger = Logger('error_growbox')
    preferences_logger = Preferences()
    preferences = preferences_logger.get_data()
    log_interval = timedelta(minutes=preferences['log_interval'])
    last_log = datetime.now()-log_interval


    def __init__(self, pin, id):
        self.pin = pin
        self.id = id
        self.state = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, True)
        Growbox.actuators.append(self)

    def set_state(self, state=False):
        self.state = state
        print(f'{self.id} set to state {self.state} and GPIO to {not self.state}')
        GPIO.output(self.pin, not self.state)

    def toggle_state(self):
        self.state = not self.set_state

    @classmethod
    def safe_preferences(cls):
        print(cls.preferences)
        cls.preferences_logger.write(cls.build_data())

    
    @classmethod
    def path_data(cls):
        return cls.data_logger.get_path()

    @staticmethod
    def get_time():
        return datetime.now()

    @classmethod
    def update_sensordata(cls):
        cls.sensordata =  Sensor.get_data()
           

    # pins = [18, 23, 24, 17, 27, 22]
    @classmethod
    def init_actuators(cls):
        print('init growbox')
        Growbox.update_sensordata()
        Lamp(24, 'lamp_g', 18 , growth_phase='g')
        Lamp(23, 'lamp_f', 12, growth_phase='f')
        Pot(22, 'pot1', 27, 'soil1')
        Pot(17, 'pot2', 27, 'soil2')
        Fan(18, 'fan')
        
        cls.update_sensordata()
        Lamp.update_lamps()
        Pot.update_pots()
        Fan.update_fans()

    @classmethod
    def log_data(cls):
        if datetime.now() >= cls.last_log + cls.log_interval:
            print("loging data")
            cls.last_log = datetime.now()
            
            cls.data_logger.write(js.dumps(cls.build_data()))

    @classmethod
    def main_loop(cls):
        print('starting growbox')
        while True:
            try:
                cls.update_sensordata()
                Lamp.update_lamps()
                Pot.update_pots()
                Fan.update_fans()
                cls.log_data()
            except Exception as e:
                cls.error_logger.write(repr(e))
                raise e
           

    @classmethod
    def build_data(cls):
        _data = {}
        _data['time'] = datetime.now().strftime("%H:%M:%S")
        _data['date'] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        _data['cpu_temp'] = cls.cpu.temperature
        _data = _data | Growbox.sensordata
        _data = _data | Lamp.get_data()
        _data = _data | Pot.get_data()
        _data = _data | Fan.get_data()
        return _data
        ## print(js.dumps(_data, indent=4))
        #exit()


class Lamp(Growbox):

    lamps = []
    phase =  Growbox.preferences['lamp_phase']
    lamp_state = False
    on_time = timedelta(hours=int(Growbox.preferences['lamp_ontime'].split(':')[0]),
                     minutes=int(Growbox.preferences['lamp_ontime'].split(':')[1])) 
   
    def __init__(self, pin, id, duration, growth_phase='g'):
        super().__init__(pin, id)
        self.duration = duration
        self.duration = timedelta(hours=duration) # time when lmap turns on
 
        
        self.growth_phase = growth_phase
        Lamp.lamps.append(self)


    @classmethod
    def get_data(cls):
        _data = {}
        _data['lamp_phase'] = cls.phase
        _data['lamp_state'] = cls.lamp_state
        _ontime = str(cls.on_time)
        if len(_ontime) < 8:
            _ontime = '0' + _ontime
        _ontime = _ontime[:_ontime.rfind(':')]

        _data['lamp_ontime']= _ontime

        for lamp in cls.lamps:
            _data[lamp.id+ '_state']=lamp.state
            _data[lamp.id+ '_duration']=lamp.duration.seconds//3600
            _data[lamp.id+ '_phase']=lamp.growth_phase
            pass
        return _data

    def update(self):
        _time =Growbox.get_time()
        day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        #turn off if not right phase
        if Lamp.phase != self.growth_phase and self.state:
            self.set_state(False)
           

        elif Lamp.phase == self.growth_phase:
             # turning off
            if self.state:
                if _time > Lamp.on_time +  self.duration + day or _time < Lamp.on_time + day:
                    self.set_state(False)
                    Lamp.lamp_state = False
                 
            # turn on
            elif not self.state and _time > Lamp.on_time + day and _time < Lamp.on_time + day +  self.duration:
                self.set_state(True)
                Lamp.lamp_state = True
             

    @classmethod
    def set_phase(cls, phase):
        cls.phase = phase
        
                
    @classmethod
    def update_lamps(cls):
        for lamp in cls.lamps:
            lamp.update()


    @classmethod
    def set_phase(cls, phase):
        cls.phase = phase # 'g' or ''f'
        

    @classmethod
    def set_starttime(cls, starttime):
        _dt = datetime.strptime(starttime, "%H:%M")
        cls.on_time = timedelta(hours=_dt.hour, minutes=_dt.minute)
        


class Pot(Growbox):
    pin_pump = 0
    state_pump= False
    pots = []
    irrigation_interval =  Growbox.preferences['irrigation_interval']  # hours
    irrigation_duration = Growbox.preferences['irrigation_duration']  # in seconds
    soil_moist_hyst_min =  Growbox.preferences['soil_moist_hyst_min']
    soil_moist_hyst_max =  Growbox.preferences['soil_moist_hyst_max']

    def __init__(self, pin, state, pin_pump, index_soil):
        super().__init__(pin, state)
        Pot.pin_pump=pin_pump
        Pot.pots.append(self)
        self. index_soil = index_soil # index for dict form sensordate (available: "soil1", "soil2", "siol3")
        self.flag_dry = False
        self.last_irrigation = datetime.now()-timedelta(hours=Pot.irrigation_interval)+ timedelta(seconds=15)
        GPIO.setup(pin_pump, GPIO.OUT)
        GPIO.output(self.pin, True)


    @classmethod
    def get_data(cls):
        _data = {}
        _data['state_pump'] = cls.state_pump
        _data['irrigation_interval'] = cls.irrigation_interval
        _data['irrigation_duration'] = cls.irrigation_duration
        _data['soil_moist_hyst_min'] = cls.soil_moist_hyst_min
        _data['soil_moist_hyst_max'] = cls.soil_moist_hyst_max
        for pot in cls.pots:
            _data[pot.id + '_state'] = pot.state
            _data[pot.id + '_dry'] = pot.flag_dry
            _data[pot.id + '_soil_moist'] = pot.soil_moist
       
        return _data

    def update(self):
        #update soil moist
        self.soil_moist = Growbox.sensordata[self.index_soil]
        # raise flag if dry
        if self.soil_moist <= Pot.soil_moist_hyst_min:
            self.flag_dry = True
        elif self.soil_moist >= Pot.soil_moist_hyst_max:
            self.flag_dry = False

        # call pummp and valve if pump state is false
        if not Pot.state_pump and self.flag_dry and datetime.now() - self.last_irrigation > timedelta(hours=Pot.irrigation_interval):
            Pot.start_time = datetime.now()
            Pot.state_pump = True
            GPIO.output(Pot.pin_pump, False) #inverted relais
            Pot.pumping_pot_id = self.id
            self.last_irrigation = datetime.now()
            self.set_state(True)
            
        elif Pot.state_pump and Pot.pumping_pot_id == self.id and datetime.now() - Pot.start_time > timedelta(seconds=self.irrigation_duration):
            Pot.state_pump = False
            GPIO.output(Pot.pin_pump, True) #inverted relais
            self.set_state(False)
            Pot.pumping_pot_id = ''
            
            
    @classmethod
    def update_pots(cls):
        for pot in cls.pots:
            pot.update()


    @classmethod
    def set_irrigation_interval(cls, irrigation_interval): # in hours
        cls.irrigation_interval = int(irrigation_interval)

    @classmethod
    def set_irrigation_duration(cls, irrigation_duration): # in seconds
        cls.irrigation_duration = int(irrigation_duration)

    @classmethod
    def set_soil_moist_hyst_min(cls, soil_moist_hyst_min): 
        cls.soil_moist_hyst_min = int(soil_moist_hyst_min)
    
    @classmethod
    def set_soil_moist_hyst_max(cls, soil_moist_hyst_max): 
        cls.soil_moist_hyst_max = int(soil_moist_hyst_max)



    
class Fan(Growbox):

    fans=[]
    temp_hyst_min = Growbox.preferences['temp_hyst_min']
    temp_hyst_max = Growbox.preferences['temp_hyst_max']
    hum_hyst_min = Growbox.preferences['hum_hyst_min']
    hum_hyst_max = Growbox.preferences['hum_hyst_max']
    fans_state = False
   
    def __init__(self, pin, id):
        super().__init__(pin, id)

        Fan.fans.append(self)
    

    @classmethod
    def get_data(cls):
        _data = {}
        _data['temp_hyst_min'] = cls.temp_hyst_min
        _data['temp_hyst_max'] = cls.temp_hyst_max
        _data['hum_hyst_min'] = cls.hum_hyst_min
        _data['hum_hyst_max'] = cls.hum_hyst_max
        _data['state'] = cls.fans_state
        for fan in cls.fans:
            _data[fan.id + '_state'] =  fan.state
        return _data

    def update(self):
        temp = int(Growbox.sensordata['temp'])
        hum = int(Growbox.sensordata['hum'])

        if not self.state:
            if temp >= Fan.temp_hyst_max or hum >= Fan.hum_hyst_max:
                self.set_state(True)
                Fan.fans_state = True
                # print(f"turning on {self.id}")
        
        elif self.state and  Fan.temp_hyst_min > temp and Fan.hum_hyst_min > hum:
                self.set_state(False)
                Fan.fans_state = False
                # print(f"turning on {self.id}") 

    @classmethod
    def update_fans(cls):
        for fan in cls.fans:
            fan.update()

    @classmethod
    def set_temp_hyst_min(cls, temp_hyst_min): 
        cls.temp_hyst_min = int(temp_hyst_min)

    @classmethod
    def set_temp_hyst_max(cls, temp_hyst_max): 
        cls.temp_hyst_max = int(temp_hyst_max)

    @classmethod
    def set_hum_hyst_min(cls, hum_hyst_min): 
        cls.hum_hyst_min = int(hum_hyst_min)

    @classmethod
    def set_hum_hyst_max(cls, hum_hyst_max): 
        cls.hum_hyst_max = int(hum_hyst_max)

 

if __name__=='__main__':

    Growbox.init_actuators()
    Growbox.safe_preferences()
    Growbox.main_loop()
    

        

  