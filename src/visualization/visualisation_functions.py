import pandas as pd
from wordcloud import WordCloud

# helper functions 
def filter_dataframe(df, state, city, neighborhood):
    dff = df[
        (df["state"] == state)
        & (df["city"] == city)
        & (df["neighbor_labels"] == neighborhood)
    ]
    return dff


def get_metrics(df):
	no_of_restaurants = len(df)
	try:
		closure_rate = round(len(df[df['is_open'] == 0]) / no_of_restaurants, 2)
	except: 
		closure_rate = 0
	ave_stars = round(df['stars_mean_restaurant'].mean(), 2)
	review_count = df['review_count'].sum()

	return no_of_restaurants, closure_rate, ave_stars, review_count
