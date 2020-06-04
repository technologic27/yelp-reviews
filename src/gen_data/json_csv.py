import collections
import csv
import json


class jsonCSV(object):

    def __init__(self, iFile, oFile):
        self.iFile = iFile
        self.oFile = oFile

    def read_write(self, column_names):
        with open(self.oFile, 'w', encoding='utf-8') as ofile:
            csv_file = csv.writer(ofile)
            csv_file.writerow(list(column_names))
            for line in self._line():
      
            	csv_file.writerow(self.get_row(line, column_names))

    def _line(self):
        with open(self.iFile) as ifile:
            for line in ifile:
                yield json.loads(line)

    def get_superset_column_names(self):
        column_names = set()
        for line in self._line():
            column_names.update(set(self.get_column_names(line).keys()))
        return column_names

    def get_column_names(self, line, parent_key=''):
        column_names = []
        for k, v in line.items():
            if parent_key:
                column_name = parent_key + "." + k
            else:
                column_name = k

            if isinstance(v, collections.MutableMapping):
                column_names.extend(self.get_column_names(v, column_name).items())
            else:
                column_names.append((column_name, v))
        return dict(column_names)

    def get_nested_value(self, d, key):


    	if "." not in key:
    		if d is None:
    			return None
    		if key not in d.keys():
    			return None
    		return d[key]


    	base_key, sub_key = key.split('.', 1)
    	if base_key not in d: 
    		return None
    	sub_dict = d[base_key]
    	return self.get_nested_value(sub_dict, sub_key)

    def get_row(self, line, column_names):
	    row = []
	    for column_name in column_names:
	        line_value = self.get_nested_value(line,column_name)
	        if isinstance(line_value, str):
	            row.append('{0}'.format(line_value))
	        elif line_value is not None:
	            row.append('{0}'.format(line_value))
	        else:
	            row.append('')
	    return row