# -*- coding: utf-8 -*-
import click
import logging
import os
from json_csv import jsonCSV


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
@click.argument('data_type', type=click.Path())
def main(input_filepath, output_filepath, data_type):
    """ Runs data processing scripts to turn source data from into
        cleaned data ready to be pushed to sql (saved in data/raw).
    """
    a = jsonCSV(input_filepath, os.path.join(output_filepath, data_type+'.csv'))
    column_names = a.get_superset_column_names()
    a.read_write(column_names)

    logger = logging.getLogger(__name__)
    logger.info('transform log files into csv')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='logs/data-transform.log', level=logging.INFO, format=log_fmt)
    main()