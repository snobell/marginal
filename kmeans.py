# coding=utf-8
from collections import defaultdict
import os
import re
import math
import random


def make_vector(s):
	pass

class Document(object):
	def __init__(self, text):
		self.text = text
		self.word_frequency = {}
		self.words = set()
		self.tf_idf = {}

		raw_word_frequency = defaultdict(int)
		total_term_count = 0
		for word in self.text.split():
			clean_word = self.cleanse(word)
			if clean_word:
				self.words.add(clean_word)
				raw_word_frequency[clean_word] += 1.0
				total_term_count += 1.0

		for word, frequency in raw_word_frequency.items():
			self.word_frequency[word] = frequency / total_term_count

	def calculate_tf_idf(self, idf):
		self.tf_idf = {}
		for word, idf in idf.items():
			if self.word_frequency.has_key(word):
				self.tf_idf[word] = self.word_frequency[word] * idf
			else:
				self.tf_idf[word] = 0

	def importance(self, word):
		if not self.tf_idf.has_key(word):
			return 0

		return self.tf_idf[word]

	def vector(self):
		return tuple(self.normalise([self.tf_idf[word] for word in sorted(self.tf_idf.keys())]))

	def __repr__(self):
		return "Document('{}')".format(self.text)


	@staticmethod
	def cleanse(word):
		stop_words = {
			'i', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'how', 'in', 'is', 'it',
			'la', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who', 'will',
			'with', 'and', 'the'
		}
		if word in stop_words:
			return None

		word = re.sub('[?;\.,:;\'\(\)&\*!"_]', '', word)
		return word.lower()

	@staticmethod
	def normalise(vector):
		ss = sum(x**2 for x in vector)
		return [x/ss for x in vector]


def calculate_idf(documents):
	document_words = defaultdict(int)
	for document in documents:
		for word in document.words:
			document_words[word] += 1

	return {word: math.log(len(documents) / documents_containing_word) for word, documents_containing_word in document_words.items()}

def search(documents, search_term):

	cleansed_term = Document.cleanse(search_term)
	terms = cleansed_term.split()

	best_match = None
	best_importance = 0
	for document in documents:

		term_importance = 0
		for term in terms:
			term_importance += document.importance(term)

		if term_importance > best_importance:
			best_match = document
			best_importance = term_importance
	return best_match


def calculate_centroid(vectors):
	if len(vectors) > 0:
		return tuple([sum([vector[x] for vector in vectors]) / len(vectors) for x in xrange(len(vectors[0]))])
	return None


def vector_distance(v1, v2):
	return math.sqrt(sum((v1[x]-v2[x])**2 for x in xrange(len(v1))))


def random_centroid(size):
	return tuple(Document.normalise([random.random() for x in xrange(size)]))


def cluster_vectors(vectors, clusters=3):
	centroids = [random_centroid(len(vectors[0])) for x in xrange(clusters)]

	clusters = [[] for x in xrange(clusters)]

	for vector in vectors:
		cluster_index = 0
		closest_distance = 0
		for index, centroid in enumerate(centroids):
			distance = vector_distance(vector, centroid)
			if distance < closest_distance:
				cluster_index = index
				closest_distance = distance
		print "vector is in cluster {}".format(cluster_index)

		clusters[cluster_index].append(vector)
		centroids[cluster_index] = calculate_centroid(clusters[cluster_index])



def load_books(books_directory):
	documents = []
	for book in os.listdir(books_directory):
		book_path = os.path.join(books_directory, book)
		if os.path.isfile(book_path):
			with open(book_path, 'r') as f:
				documents.append(Document(f.read()))

	process_documents(documents)

	return documents


def process_documents(documents):
	word_idf = calculate_idf(documents)

	for document in documents:
		document.calculate_tf_idf(word_idf)


def main2():
	documents = load_books('/Users/chris/Downloads/books')

	vectors = [document.vector() for document in documents]

	cluster_vectors(vectors)



	while True:
		search_term = raw_input("Search: ")
		print search(documents, search_term)


def main():
	documents = [
		Document("The quick brown fox jumps over the lazy dog."),

		Document("""Illiteracy is the inability to read and write.
		Though the percent of sufferers has halved in the last
		35 years, currently 15% of the world has this affliction.
		Innumeracy is the inability to apply simple numerical
		concepts. The rate of innumeracy is unknown but chances
		are that it affects over 50% of us. This tragedy impedes
		our ability to have a discourse on matters related to
		quantitative judgement while policy decisions
		increasingly depend on this judgement."""),

		Document("""The Internet is where all conversation about
		normcore seems to converge. New media has changed our
		relation to information, and, with it, fashion. Reverse
		Google Image Search and tools like Polyvore make
		discovering the source of any garment as simple as a
		few clicks. Online shopping—from eBay through the
		Outnet—makes each season available for resale almost
		as soon as it goes on sale. As Natasha Stagg, the
		Online Editor of V Magazine and a regular contributor
		at DIS (where she recently wrote a normcore-esque essay
		about the queer appropriation of mall favorite
		Abercrombie & Fitch), put it: “Everyone is a researcher
		and a statistician now, knowing accidentally the
		popularity of every image they are presented with, and
		what gets its own life as a trend or meme.” The cycles
		of fashion are so fast and so vast, it’s impossible to
		stay current; in fact, there is no one current. Passing around the buck."""),

		Document("""Note that the taxonomy has a hierarchy. Creations are novel, inventions are creations and innovations are usually based on some invention. However inventions are not innovations and neither are creations or novelties. Innovations are therefore the most demanding works because they require all the conditions in the hierarchy. Innovations implicitly require defensibility through a unique “operating model”. Put another way, they remain unique because few others can copy them.
To be innovative is very difficult, but because of the difficulty, being innovative is usually well rewarded. Indeed, it might be easier to identify innovations simply by their rewards. It’s almost a certainty that any great business is predicated on an innovation and that the lack of a reward in business means that some aspect of the conditions of innovation were not met.
The causal, if-and-only-if connection with reward is what should be the innovation litmus test. If something fails to change the world (and hence is unrewarded) you can be pretty sure it was not innovative enough.
Which brings us to the quote above. The fact that the Nokia tablet of 2001 not only did not succeed in the market but was not even released implies that it could not have been innovative. The product was only at the stage of perhaps being an invention (if it can be shown to be unique) or merely a creation (if it isn’t.) Furthermore, if the product is so poorly designed that it is literally unusable then it is just a novelty. A design, sketch or verbal description might be novel but it does not qualify as an innovation or an invention or even a creation. How far the depiction went toward making a dent in the universe defines its innovativeness.
Why does this matter?
Understanding that innovation requires passing a market test and that passing that test is immensely rewarding both for the creator and for society at large means that we can focus on how to make it happen. Obsessing over the mere novelties or inventions means we allocate resources which markets won’t reward. Misusing the term and confusing it with activities that don’t create value takes our eye off the causes and moves us away from finding ways of repeatably succeeding.
Recognizing that innoveracy is a problem allows us to address it. Addressing it would mean we could speak a language of value creation that everyone understands.
Wouldn’t that be novel? foal""")
	]

	process_documents(documents)

	print search(documents, "fact")


if __name__ == '__main__':
	main2()