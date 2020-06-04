#!/bin/bash
#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = /Users/estherdawes/Downloads/yelp-dataset
PROFILE = default
PROJECT_NAME = yelp-reviews-analytics
PYTHON_INTERPRETER = python

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies

setup:
	$ pip install virtualenv
	$ virtualenv yelp-reviews

activate:
	$ source yelp-reviews/bin/activate
	$ pip install -r requirements.txt

## Make Dataset
data_business:
	$(PYTHON_INTERPRETER) src/gen_data/make_dataset.py $(BUCKET)/yelp_academic_dataset_business.json data/raw business

data_review:
	$(PYTHON_INTERPRETER) src/gen_data/make_dataset.py $(BUCKET)/yelp_academic_dataset_review.json data/raw review

data_checkin:
	$(PYTHON_INTERPRETER) src/gen_data/make_dataset.py $(BUCKET)/yelp_academic_dataset_checkin.json data/raw checkin

data_user:
	$(PYTHON_INTERPRETER) src/gen_data/make_dataset.py $(BUCKET)/yelp_academic_dataset_user.json data/raw user

features:
	$(PYTHON_INTERPRETER) src/features/make_features_dataset.py data/raw data/processed

train:
	$(PYTHON_INTERPRETER) src/models/train_test.py models/output models/model data/processed

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already installed.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py