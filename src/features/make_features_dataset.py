from combine_features import CombineFeatures
import pandas as pd
import click
import os
import logging


@click.command()
@click.argument('input_filepath', type=click.Path())
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Create features from data/raw and saves csv into data/processed
    """
    df_bus = pd.read_csv(os.path.join(input_filepath, 'business.csv'))
    df_rev = pd.read_csv(os.path.join(input_filepath, 'review.csv'))

    df_bus_select = df_bus[['is_open', 'state', 'city', 'business_id', 'stars', 'longitude', 'latitude', 'categories', 'review_count']]
    df_rev_select = df_rev[['business_id', 'stars', 'date']]
    category_list = ['Thai']

    combiner = CombineFeatures(df_bus_select, df_rev_select, category_list, add_categories=False)
    df = combiner.transform()
    df.to_csv(os.path.join(output_filepath,'features.csv'), index=False)

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='logs/data-transform.log', level=logging.INFO, format=log_fmt)
    main()