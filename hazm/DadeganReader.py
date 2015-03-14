# coding: utf8

from __future__ import unicode_literals
import codecs
from nltk.parse import DependencyGraph
from nltk.tree import Tree


def coarse_pos_e(tags):
	"""
	Coarse POS tags of Dadegan corpus:
		N: Noun, V: Verb, ADJ: Adjective, ADV: Adverb, PR: Pronoun, PREP: Preposition, POSTP: Postposition, CONJ: Conjunction, PUNC: Punctuation, ADR: Address Term, IDEN: Title, PART: Particle, POSNUM: Post-noun Modifier, PREM: Pre-modifier, PRENUM: Pre-noun Numeral, PSUS: Pseudo-sentence, SUBR: Subordinating Clause

	>>> coarse_pos_e(['N', 'IANM'])
	'N'
	"""

	map = {'N': 'N', 'V': 'V', 'ADJ': 'AJ', 'ADV': 'ADV', 'PR': 'PRO', 'PREM': 'DET', 'PREP': 'P', 'POSTP': 'POSTP', 'PRENUM': 'NUM', 'CONJ': 'CONJ', 'PUNC': 'PUNC', 'SUBR': 'CONJ'}
	return map.get(tags[0], 'X') + ('e' if 'EZ' in tags else '')


word_nodes = lambda tree: list(tree.nodes.values())[1:]
node_deps = lambda node: sum(node['deps'].values(), [])


class DadeganReader():
	"""
	interfaces [Persian Dependency Treebank](http://dadegan.ir/perdt/download)

	>>> dadegan = DadeganReader(conll_file='corpora/dadegan.conll')
	>>> next(dadegan.sents())
	[('این', 'DET'), ('میهمانی', 'N'), ('به', 'P'), ('منظور', 'Ne'), ('آشنایی', 'Ne'), ('هم‌تیمی‌های', 'Ne'), ('او', 'PRO'), ('با', 'P'), ('غذاهای', 'Ne'), ('ایرانی', 'AJ'), ('ترتیب', 'N'), ('داده_شد', 'V'), ('.', 'PUNC')]

	>>> from hazm.Chunker import tree2brackets
	>>> tree2brackets(next(dadegan.chunked_trees()))
	'[این میهمانی NP] [به PP] [منظور آشنایی هم‌تیمی‌های او NP] [با PP] [غذاهای ایرانی NP] [ترتیب داده_شد VP] .'
	"""

	def __init__(self, conll_file, pos_map=coarse_pos_e):
		self._conll_file = conll_file
		self._pos_map = pos_map if pos_map else lambda tags: ','.join(tags)

	def _sentences(self):
		with codecs.open(self._conll_file, encoding='utf8') as conll_file:
			text = conll_file.read()

			# refine text
			text = text.replace('‌‌', '‌').replace('\t‌', '\t').replace('‌\t', '\t').replace('\t ', '\t').replace(' \t', '\t').replace(
				'\r', '').replace('\u2029', '‌')

			for item in text.replace(' ', '_').split('\n\n'):
				if item.strip():
					yield item

	def trees(self):
		for sentence in self._sentences():
			tree = DependencyGraph(sentence)

			for node in word_nodes(tree):
				node['mtag'] = [node['ctag'], node['tag']]

			for node in word_nodes(tree):
				if node['rel'] in {'MOZ', 'NPOSTMOD', 'NEZ'} and tree.nodes[node['head']]['ctag'] in {'N', 'ADJ', 'PR', 'ADV', 'POSNUM', 'PREP'}:
					if node['head'] != node['address'] - 1:
						head = tree.nodes[node['head']]
						hasConj = False
						for dep in node_deps(head):
							if tree.nodes[dep]['rel'] in ('NCONJ',):
								hasConj = True
								for conj in node_deps(tree.nodes[dep]):
									if tree.nodes[conj]['rel'] == 'POSDEP':
										tree.nodes[conj]['mtag'].append('EZ')
										break
								break

						deps = node_deps(head)
						while len(deps) > 0:
							dep = deps.pop()
							if dep == tree.nodes[dep]['head'] + 1:
								deps = node_deps(tree.nodes[dep])
								if len(deps) == 0:
									tree.nodes[dep]['mtag'].append('EZ')

						if hasConj is True:
							continue

					tree.nodes[node['head']]['mtag'].append('EZ')
					if node['head'] < node['address'] - 1:
						if node['rel'] == 'MOZ' and tree.nodes[node['address'] - 1]['rel'] == 'NPOSTMOD':
							tree.nodes[node['address'] - 1]['mtag'].append('EZ')
			for node in word_nodes(tree):
				node['mtag'] = self._pos_map(node['mtag'])

			yield tree

	def sents(self):
		for tree in self.trees():
			yield [(node['word'], node['mtag']) for node in word_nodes(tree)]

	def chunked_trees(self):
		for tree in self.trees():
			chunks = []
			for node in word_nodes(tree):
				n = node['address']
				item = (node['word'], node['mtag'])
				appended = False
				if node['ctag'] in {'PREP', 'POSTP'}:
					for d in node_deps(node):
						label = 'PP'
						if node['ctag'] == 'POSTP':
							label = 'POSTP'
						if d == n - 1 and type(chunks[-1]) == Tree and chunks[-1].label() == label:
							chunks[-1].append(item)
							appended = True
					if node['head'] == n - 1 and len(chunks) > 0 and type(chunks[-1]) == Tree and chunks[
						-1].label() == label:
						chunks[-1].append(item)
						appended = True
					if not appended:
						chunks.append(Tree(label, [item]))
				elif node['ctag'] in {'PUNC', 'CONJ', 'SUBR', 'PART'}:
					if item[0] in {"'", '"', '(', ')', '{', '}', '[', ']', '-', '#', '«', '»'} and len(chunks) > 0 and type(chunks[-1]) == Tree:
						for l in chunks[-1].leaves():
							if l[1] == item[1]:
								chunks[-1].append(item)
								appended = True
								break
					if appended is not True:
						chunks.append(item)
				elif node['ctag'] in {'N', 'PREM', 'ADJ', 'PR', 'ADR', 'PRENUM', 'IDEN', 'POSNUM', 'SADV'}:
					if node['rel'] in {'MOZ', 'NPOSTMOD'}:
						if len(chunks) > 0:
							if type(chunks[-1]) == Tree:
								j = n - len(chunks[-1].leaves())
								chunks[-1].append(item)
							else:
								j = n - 1
								treeNode = Tree('NP', [chunks.pop(), item])
								chunks.append(treeNode)
							while j > node['head']:
								leaves = chunks.pop().leaves()
								if len(chunks) < 1:
									chunks.append(Tree('NP', leaves))
									j -= 1
								elif type(chunks[-1]) == Tree:
									j -= len(chunks[-1])
									for l in leaves:
										chunks[-1].append(l)
								else:
									leaves.insert(0, chunks.pop())
									chunks.append(Tree('NP', leaves))
									j -= 1
							continue
					elif node['rel'] == 'POSDEP' and tree.nodes[node['head']]['rel'] in {'NCONJ', 'AJCONJ'}:
						conj = tree.nodes[node['head']]
						if tree.nodes[conj['head']]['rel'] in {'MOZ', 'NPOSTMOD', 'AJCONJ', 'POSDEP'}:
							label = 'NP'
							leaves = [item]
							j = n - 1
							while j >= conj['head']:
								if type(chunks[-1]) is Tree:
									j -= len(chunks[-1].leaves())
									label = chunks[-1].label()
									leaves = chunks.pop().leaves() + leaves
								else:
									leaves.insert(0, chunks.pop())
									j -= 1
							chunks.append(Tree(label, leaves))
							appended = True
					elif node['head'] == n - 1 and len(chunks) > 0 and type(chunks[-1]) == Tree and not chunks[
						-1].label() == 'PP':
						chunks[-1].append(item)
						appended = True
					elif node['rel'] == 'AJCONJ' and tree.nodes[node['head']]['rel'] in {'NPOSTMOD', 'AJCONJ'}:
						np_nodes = [item]
						label = 'ADJP'
						i = n - node['head']
						while i > 0:
							if type(chunks[-1]) == Tree:
								label = chunks[-1].label()
								leaves = chunks.pop().leaves()
								i -= len(leaves)
								np_nodes = leaves + np_nodes
							else:
								i -= 1
								np_nodes.insert(0, chunks.pop())
						chunks.append(Tree(label, np_nodes))
						appended = True
					elif node['ctag'] == 'ADJ' and node['rel'] == 'POSDEP' and tree.nodes[node['head']]['ctag'] != 'CONJ':
						np_nodes = [item]
						i = n - node['head']
						while i > 0:
							label = 'ADJP'
							if type(chunks[-1]) == Tree:
								label = chunks[-1].label()
								leaves = chunks.pop().leaves()
								i -= len(leaves)
								np_nodes = leaves + np_nodes
							else:
								i -= 1
								np_nodes.insert(0, chunks.pop())
						chunks.append(Tree(label, np_nodes))
						appended = True
					for d in node_deps(node):
						if d == n - 1 and type(chunks[-1]) == Tree and chunks[
							-1].label() != 'PP' and appended is not True:
							label = chunks[-1].label()
							if node['rel'] == 'ADV':
								label = 'ADVP'
							elif label in {'ADJP', 'ADVP'}:
								if node['ctag'] == 'N':
									label = 'NP'
								elif node['ctag'] == 'ADJ':
									label = 'ADJP'
							leaves = chunks.pop().leaves()
							leaves.append(item)
							chunks.append(Tree(label, leaves))
							appended = True
						elif tree.nodes[d]['rel'] == 'NPREMOD' and appended is not True:
							np_nodes = [item]
							i = n - d
							while i > 0:
								if type(chunks[-1]) == Tree:
									leaves = chunks.pop().leaves()
									i -= len(leaves)
									np_nodes = leaves + np_nodes
								else:
									i -= 1
									np_nodes.insert(0, chunks.pop())
							chunks.append(Tree('NP', np_nodes))
							appended = True
					if not appended:
						label = 'NP'
						if node['ctag'] == 'ADJ':
							label = 'ADJP'
						elif node['rel'] == 'ADV':
							label = 'ADVP'
						chunks.append(Tree(label, [item]))
				elif node['ctag'] in {'V'}:
					appended = False
					for d in node_deps(node):
						if d == n - 1 and type(chunks[-1]) == Tree and tree.nodes[d]['rel'] in {'NVE', 'ENC'} and appended is not True:
							leaves = chunks.pop().leaves()
							leaves.append(item)
							chunks.append(Tree('VP', leaves))
							appended = True
						elif tree.nodes[d]['rel'] in {'VPRT', 'NVE'}:
							vp_nodes = [item]
							i = n - d
							while i > 0:
								if type(chunks[-1]) == Tree:
									leaves = chunks.pop().leaves()
									i -= len(leaves)
									vp_nodes = leaves + vp_nodes
								else:
									i -= 1
									vp_nodes.insert(0, chunks.pop())
							chunks.append(Tree('VP', vp_nodes))
							appended = True
							break
					if not appended:
						chunks.append(Tree('VP', [item]))
				elif node['ctag'] in {'PSUS'}:
					if node['rel'] == 'ADV':
						chunks.append(Tree('ADVP', [item]))
					else:
						chunks.append(Tree('VP', [item]))
				elif node['ctag'] in {'ADV', 'SADV'}:
					appended = False
					for d in node_deps(node):
						if d == n - 1 and type(chunks[-1]) == Tree:
							leaves = chunks.pop().leaves()
							leaves.append(item)
							chunks.append(Tree('ADVP', leaves))
							appended = True
					if not appended:
						chunks.append(Tree('ADVP', [item]))

			yield Tree('S', chunks)
