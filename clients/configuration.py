import configparser

import logging
logging.basicConfig(
    format='%(asctime)s [%(filename)s:%(lineno)s - %(module)s:%(funcName)10s() : %(levelname)s] %(message)s', level=logging.INFO)


class Configuration(object):
    log = None

    config_parser = None
    configuration_file = None

    def __init__(self, configuration_file_name):
        self.log = logging.getLogger(self.__class__.__name__)

        self.configuration_file = configuration_file_name
        self.config_parser = configparser.ConfigParser()
        files_read = self.config_parser.read(self.configuration_file)

    def get_option(self, section, option):

        if self.config_parser.has_section(section) is False:
            self.log.warning(
                'Cannot find in the configuration the section: %s', section)
            return None

        if self.config_parser.has_option(section, option) is False:
            self.log.warning(
                'Cannot find in the configuration under the section %s the option: %s', section, option)
            return None

        return self.config_parser.get(section, option)

    def get_section(self, section):

        if self.config_parser.has_section(section) is False:
            self.log.warning(
                'Cannot find in the configuration the section: %s', section)
            return None

        section_properties = self.config_parser.items(section)
        result = {}
        if section_properties is not None:
            for property, value in section_properties:
                result[property] = value

        return result
