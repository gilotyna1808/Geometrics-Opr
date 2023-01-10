import configparser
from os.path import exists

class geometrics_config():

    def __init__(self):
        self.config_file_path = 'config.ini'
        self.config = None
        if(exists(self.config_file_path)):
            # self.create_config()
            self.load_config()
            self.check_config_file()
        else:
            raise Exception("Not implemented")
    
    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        self.config.sections()
        
    def load_value_from_config_str(self, section, attr):
        if(section in self.config):
            if(attr in self.config[section]):
                return self.config.get(section, attr)
        raise Exception(f"Nie ma attrybutu {section} {attr}")

    def load_value_from_config_int(self, section, attr):
        if(section in self.config):
            if(attr in self.config[section]):
                return self.config.getint(section, attr)
        raise Exception(f"Nie ma attrybutu {section} {attr}")
    
    def load_value_from_config_bool(self, section, attr):
        if(section in self.config):
            if(attr in self.config[section]):
                return self.config.getboolean(section, attr)
        raise Exception(f"Nie ma attrybutu {section} {attr}")
    
    def create_config(self):
        config = configparser.ConfigParser()
        config['file_dir'] = {}
        config['file_dir']['data_bin'] = 'bin'
        config['file_dir']['data_mag_values'] = 'data'
        config['file_dir']['data_mag_statuses'] = 'status'
        config['program'] = {}
        config['program']['silent'] = 'False'
        config['program']['time_to_new_file'] = '600'
        config['rs232_settings'] = {}
        config['rs232_settings']['port'] = '/dev/ttyUSB0'
        config['rs232_settings']['baudrate'] = str(115200)
        config['rs232_settings']['timeout'] = str(1)
        with open(self.config_file_path, 'w') as configfile:
          config.write(configfile)
    
    def check_config_file(self):
        section_list = {}
        # section_list['file_dir'] = ['Log','Data']
        section_list['program'] = ['silent']
        section_list['rs232_settings'] = ['port','baudrate','timeout']
        for section in section_list:
            if(self.check_if_section_exist(section) is False):
                raise Exception(f'Brak sekcji {section}')
            for attr in section_list[section]:
                if(self.check_if_attr_exist(section, attr) is False):
                    raise Exception(f'Brak atrybutu {attr} w sekcji {attr}')
    
    def save_config(self):
        config = configparser.ConfigParser()
        for section in self.config:
            if section != 'DEFAULT':
              config[section] = {}
              for attr in self.config[section]:
                  config[section][attr] = self.config[section][attr]
        
        with open(self.config_file_path, 'w') as configfile:
          config.write(configfile)

    def check_if_section_exist(self, section):
        return section in self.config
    
    def check_if_attr_exist(self, section, attr):
        return attr in self.config[section]