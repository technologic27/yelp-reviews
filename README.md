# Yelp Restaurant Closure Prediction
==============================


# Installation

Requires Python3.+ to run.

Change directory to the project directory.

```sh
cd path/to/project_directory
```
Set-up virtual environment for the first time.

```sh
$ make setup
```
Activate virtual environment.

```sh
$ source yelp-reviews/bin/activate
```
Install requirements.

```sh
sudo pip install -r requirements.txt
```
Change global variable `BUCKET` in `Makefile` to the file directory that contains the raw yelp dataset in json format

Create clean dataset for metrics generation and modelling. Do this only once!

```sh
$ make data_business
$ make data_review
$ make data_checkin
$ make data_user
```
Generate features for modelling.

```sh
$ make features
```
Train the machine learning models

```sh
$ make train
```

If virtual environment `yelp-reviews` has been created before, activate virtual environment using the following command. Skip installation of requirements.

```sh
$ source yelp-reviews/bin/activate
```
The model evaluation, business metric calculation and visualisation is in `notebooks/` directory. To activate jupyter notebook, type the following command

```sh
$ jupyter notebooks
```

# File Submission Information
Business Use Case
---
I have used the business and review dataset to predict the closure of a restaurant, where the postive outcome is the restaurant remains opens and the negative outcome is the closure of the restaurant. For this classificaion problem, I used a decision tree, random forest and gradient boosting classifier. The models artefacts are located in `models/model/`. The model prediction results are located in `models/output/`. A quick overview of the average model results is as follows:

1. Accuracy:  ~ 71%
2. Precision:  ~ 75%
3. Recall:  ~ 93%
4. F1 Score:  ~ 80%


Deep-dive Analysis of model and feature importance
---
Results of the model are in the notebooks directory.
`notebooks/model_evaluation.ipynb`

Visualisation of Business Metrics for decision making
---
`notebooks/visualisations.ipynb`

MySQL database connector
---
`clients/`

SQL queries to create schema, push data into the DB and generate metrics
---
`sql_scripts/`


Data Details
---
Raw data is found in `data/raw`. Cleaned for the interim data is found in `data/interim` and data used for metric generation and modelling is found in `data/processed`. If the data has been generated, skip `make data_*` step.


### Improvements

 - Write pytests to ensure reproducibility
 - Documentation for Sphinx
 - Additional logging to track model
 - YAML file to store ML model parameters
 - Generate more features to improve model performance
 - Create a visualisation dashboard
 - Containerize solution to serve and deploy models
 - Develop a model selection strategy

### Credits

