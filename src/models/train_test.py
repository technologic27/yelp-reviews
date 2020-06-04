import os
import click
import pickle
import json
import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
from select_dataframe import DataFrameSelector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, confusion_matrix, roc_curve, precision_score, recall_score

category_list = ['Thai']
num_features = ['stars_mean_neighborhood', 'stars_mean_restaurant', 'stars_coef', 'popularity']
cat_features = ['neighbor_labels', 'is_above_average']
label = ['is_open']


def scale_data(num_features, cat_features, y_label, df):
    num_pipeline = Pipeline([
        ('selector', DataFrameSelector(num_features)),
        ('std_scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('selector', DataFrameSelector(cat_features)),
    ])

    full_pipeline = FeatureUnion([
        ('num_pipeline', num_pipeline),
        ('cat_pipeline', cat_pipeline)
    ])

    X = full_pipeline.fit_transform(df)
    y = df[label].values.ravel()

    return X, y


def train_test(X, y, test_size=0.3):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42)

    return X_train, X_test, y_train, y_test


def train_gridSearch(X_train, y_train, X_test, estimator, param):

    param_grid = {
        'rf': [{
            'n_estimators': range(20, 81, 10)
        }, {
            'bootstrap': ['False'],
            'n_estimators': range(20, 81, 10)
        }],

        'dt': [{
            'max_depth': range(1, 10),
            'min_samples_leaf': [10, 20, 50, 100]
        }],

        'gb': [{
            'n_estimators': range(20, 81, 10)
        }]
    }
    grid_search = GridSearchCV(estimator, param_grid[param], cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    model = grid_search.best_estimator_
    predictions = model.predict(X_test)
    return model, predictions


def save_model(model, model_name, model_output_filepath):
    full_path = os.path.join(model_output_filepath, model_name)
    pickle.dump(model, open(full_path, 'wb'))


def save_output(X_test, y_pred_test, y_test, output_name, output_filepath):
    results = {"y_pred_test": y_pred_test.tolist(
    ), "y_test": y_test.tolist(), "X_test": X_test.tolist()}
    with open(os.path.join(output_filepath, output_name), 'w') as ofile:
        json.dump(results, ofile)


@click.command()
@click.argument('output_filepath', type=click.Path())
@click.argument('model_output_filepath', type=click.Path())
@click.argument('data_filepath', type=click.Path())
def main(output_filepath, model_output_filepath, data_filepath):

    df = pd.read_csv(os.path.join(data_filepath, 'features.csv'))

    X, y = scale_data(num_features, cat_features, label, df)

    X_train, X_test, y_train, y_test = train_test(X, y, test_size=0.3)

    clf_dt = DecisionTreeClassifier()

    dt_model, dt_pred = train_gridSearch(
        X_train, y_train, X_test, clf_dt, 'dt')

    print('--Decision Tree Results--')
    print('Accuracy: ', dt_model.score(X_test, list(y_test)))
    print('Precision: ', precision_score(list(y_test), dt_pred))
    print('Recall: ', recall_score(list(y_test), dt_pred))
    print('F1 Score: ', f1_score(list(y_test), dt_pred))
    print('Confusion Matrix: \n', confusion_matrix(list(y_test), dt_pred))

    clf_rf = RandomForestClassifier(max_features='auto', min_samples_leaf=50)

    rf_model, rf_pred = train_gridSearch(
        X_train, y_train, X_test, clf_rf, 'rf')

    print('--Random Forest Results--')
    print('Accuracy: ', rf_model.score(X_test, list(y_test)))
    print('Precision: ', precision_score(list(y_test), rf_pred))
    print('Recall: ', recall_score(list(y_test), rf_pred))
    print('F1 Score: ', f1_score(list(y_test), rf_pred))
    print('Confusion Matrix: \n', confusion_matrix(list(y_test), rf_pred))

    clf_gb = GradientBoostingClassifier(
        learning_rate=0.1,
        min_samples_split=500,
        min_samples_leaf=50,
        max_depth=8,
        max_features='auto',
        subsample=0.8,
        random_state=10
    )

    gb_model, gb_pred = train_gridSearch(
        X_train, y_train, X_test, clf_gb, 'gb')

    print('--Gradient Boosting Results--')
    print('Accuracy: ', gb_model.score(X_test, list(y_test)))
    print('Precision: ', precision_score(list(y_test), gb_pred))
    print('Recall: ', recall_score(list(y_test), gb_pred))
    print('F1 Score: ', f1_score(list(y_test), gb_pred))
    print('Confusion Matrix: \n', confusion_matrix(list(y_test), gb_pred))

    save_model(dt_model, 'dt.sav', model_output_filepath)
    save_model(rf_model, 'rf.sav', model_output_filepath)
    save_model(gb_model, 'gb.sav', model_output_filepath)

    save_output(X_test, dt_pred, y_test, 'dt.json', output_filepath)
    save_output(X_test, rf_pred, y_test, 'rf.json', output_filepath)
    save_output(X_test, gb_pred, y_test, 'gb.json', output_filepath)

if __name__ == "__main__":
    main()
