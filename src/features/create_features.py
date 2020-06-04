import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import DBSCAN


class getFeatures:

    def __init__(self, category_list):
        self.top_cats = category_list

    def get_business(self, df_bus):
        df_bus.dropna(inplace=True)
        df_bus['is_restaurant'] = df_bus['categories'].str.split(
            ',').apply(lambda x: self._category_exists(x, 'Restaurants'))
        return df_bus[df_bus['is_restaurant'] == 1]

    def neighborhood(self, df):
        kms_per_radian = 6371.0088
        epsilon = 5.0 / kms_per_radian
        coords = df[['latitude', 'longitude']].to_numpy()
        db = DBSCAN(eps=epsilon, min_samples=5, algorithm='ball_tree',
                    metric='haversine').fit(np.radians(coords))
        df['neighbor_labels'] = db.labels_
        return df

    def popularity(self, df):
        df['popularity'] = df['stars'] * df['review_count']
        return df

    def _category_exists(self, x, category):
        x = [i.strip() for i in x]
        if category in x:
            return 1
        else:
            return 0

    def categories(self, df):
        df['categories_list'] = df['categories'].str.split(",")
        for cat in self.top_cats:
            column_name = 'is_' + cat
            df[column_name] = df['categories_list'].apply(
                lambda x: self._category_exists(x, cat))
        df.drop('catgories_list', axis=1, inplace=True)
        return df

    def get_review(self, df_rest_bus, df_rev):
        df_rev.dropna(inplace=True)
        df_rev['date'] = pd.to_datetime(df_rev['date'])
        return df_rest_bus[['business_id']].merge(df_rev, how='left', on='business_id')

    def stars_daily_stats(self, df):
        df = df.groupby(['business_id', pd.Grouper(key='date', freq='D')]).aggregate(
            {'stars': ['mean', 'median']}).reset_index()
        df.columns = df.columns.droplevel(1)
        df.columns = ['business_id', 'date', 'stars_mean', 'stars_median']
        return df

    def stars_lr(self, df):
        df = df.set_index(['date'])
        df['days'] = df.groupby('business_id').apply(
            lambda x: (x.index - x.index[0]).days).explode().values
        stars_coef = df.groupby('business_id').apply(lambda x: LinearRegression().fit(
            x.days.values.reshape(-1, 1), x.stars_mean.values).coef_[0]).reset_index()
        stars_coef.columns = ['business_id', 'stars_coef']
        return df.merge(stars_coef, on='business_id')

    def stars_neighbor_stats(self, df):
        return df.groupby('neighbor_labels').mean()['stars_mean'].reset_index()

    def is_above_average(self, df):
        df['is_above_average'] = np.where(df['stars_mean_neighborhood'] < df[
                                          'stars_mean_restaurant'], 1, 0)
        return df

    def combine(self, df_rev_gen, df_bus_gen):
        df = df_rev_gen.groupby('business_id').mean().reset_index().merge(
            df_bus_gen, how='right', on='business_id')
        df = df.groupby('neighbor_labels').mean()['stars_mean'].reset_index().merge(
            df, how='right', on='neighbor_labels')
        df.rename(columns={"stars_mean_x": "stars_mean_neighborhood",
                           "stars_mean_y": "stars_mean_restaurant"}, inplace=True)
        return self.is_above_average(df)
