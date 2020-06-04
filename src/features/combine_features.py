from create_features import getFeatures
from sklearn.base import BaseEstimator, TransformerMixin


class CombineFeatures(BaseEstimator, TransformerMixin):

	def __init__(self, df_bus, df_rev, category_list, add_categories=True):
		self.add_categories = add_categories
		self.category_list = category_list
		self.df_bus = df_bus
		self.df_rev = df_rev

	def fit(self):
		return self

	def transform(self):
		a = getFeatures(self.category_list)

		dfb = a.get_business(self.df_bus)
		dfb = a.neighborhood(dfb)
		dfb = a.popularity(dfb)

		if self.add_categories:
			dfb = a.categories(dfb)

		dfr = a.get_review(dfb, self.df_rev)
		dfr = a.stars_daily_stats(dfr)
		dfr = a.stars_lr(dfr)
		return a.combine(dfr, dfb)