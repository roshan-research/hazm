
from nltk.tag.stanford import POSTagger
import subprocess

class POSTagger(POSTagger):

	@staticmethod
	def train(train_file, model_name, properties_file='resources/persian-left3words-distsim.tagger.props', path_to_jar='resources/stanford-postagger.jar', debug=False):
		cmd = [	'java', '-classpath', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger',
				'-prop', properties_file,
				'-model', model_name, 
				'-trainFile', train_file,
				'-tagSeparator', '/']
		output=subprocess.PIPE
		if (debug == True):
			p = subprocess.Popen(cmd)
		else:
			p = subprocess.Popen(cmd, stdout=output, stderr=output)