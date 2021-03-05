from gensim import models

class w2v_model(object):

	def __init__(self,config):
        self.config      = config
		self.model       = models.word2vec.Word2Vec(min_count=1)
		self.model_check = False
		self.sentences   = None
		self.epoch       = 20

	def load_sentence(self,input_file_name):
		self.sentences = models.word2vec.LineSentence(input_file_name)

	def build_vocab(self):
		self.model.build_vocab(self.sentences)

	def train(self):
		self.model.train(
			self.sentences,
			total_examples=self.model.corpus_count,
			epochs=self.epoch)

	def save_model(self,output_file_name):
		self.model.save(output_file_name)

	def make_model_and_save(self,input_file_name,output_file_name):

		self.load_sentence(input_file_name)
		self.build_vocab()
		self.train()
		self.save_model(output_file_name)
		self.model_check = True

	def load_model(self,model_file_name):
		self.model = models.word2vec.Word2Vec.load(model_file_name)
		self.model_check = True

	def most_similar(self,positive_words,negative_words,count):

		if not self.model_check:
			print ("Model is not checked, make or load the model")
			return False

		return self.model.wv.most_similar(positive_words,negative_words,count)

    def get_simliar_words(postive_words,negative_words,type):

        w2v_model = w2v_train.w2v_model()

        w2v_model.load_model("./word2vec/model/wiki.txt")

        result = w2v_model.most_similar(positive_words,negative_words,500)

        if(type == "word-only"):
            result = word_only(result)

        return result

    def w2v_train_data():

        input_text  = "./crawler/data/wiki.txt"

        output_text = "./word2vec/model/wiki.txt"

        w2v_model   = w2v_train.w2v_model()

        w2v_model.make_model_and_save(input_text,output_text)

        return

    def word_only(words_list):
        result = []
        for word_tuple in words_list:
            result.append(word_tuple[0])
        return result
