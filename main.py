import argparse
import sys

from .general_use import Config,Pro_Set
from .nlp import nlp


def initialize_pro_set():

	config     = Config()
	nlp_module = nlp.NLP(config)
	pro_set    = Pro_Set(config,nlp_module)
#	result = pro_set.make_problems(input_sentences)
	return pro_set

def load_data(module):
	module.load_data()

def problem_generation(module,input_sentences):
	result = module.make_problems(input_sentences)
	return result
