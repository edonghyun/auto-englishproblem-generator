from .word2vec import word2vec
from .nlp import nlp

import re
import py_stringmatching as sm
import jellyfish as jf
import random

class Config():
    """
        Global Configuration
    """
    def __init__(self):
        self.config = None

    # problem & question details
    number_of_sample_words   = None
    number_of_result_choices = 6

    word_blank  = "(_______________)"

    # data path
    global_text       = "./engine/crawler/data/wiki.txt"
    nlp_text          = "./engine/nlp/data/"
    word2vec_model    = "./engine/word2vec/model/w2v_0506"
    phonetic_matching = "./engine/phonetic/phonetic_matching.txt"

    # input_sentences
    input_path     = "./input_text.txt"
    output_path    = "./output_text.txt"

class Pro_Set(Config):

    def __init__(self,config,nlp):

        self.config = config
        self.nlp    = nlp

        #
        self.input_sentences    = None

        #
        self.word2vec_model     = None
        self.word_dictionary    = None
        self.phonetic_matching  = None

        # result of Making Problems
        self.tokenized_sentence = None
        self.without_stopwords  = None
        self.possible_blank_pos = None
        self.semantic_choices   = None
        self.sound_choices      = None

        self.result_problem_set = None

    def load_data(self):

        self.load_word_dictionary()
        self.word2vec_load()

    def make_problems(self,input_sentences):
        """
            main functions of making problems.
            first, build problem sets
            second, project those problem sets
        """
        self.load_input_text(input_sentences)

        # build
        self.voca_check(self.input_sentences,self.word_dictionary)
        self.generate_semantic_choices()
        self.generate_sound_choices()
        self.choices_intersection()

        # project
        result = self.project_problem_set()

        return result

    def load_input_text(self,input_sentences):
        """

        """
        # f = open(self.config.input_path)

        # line = f.read()
        replaced = input_sentences.replace("_"," ")

        sentences = 	re.sub(r'[^a-zA-Z0-9?\"\'=\.\,]',' ', replaced)

        self.input_sentences = sentences

    def load_word_dictionary(self):

        self.word_dictionary = self.nlp.word_dictionary()

    def word2vec_load(self):
        """
            Model is placed in the word2vec directory.
        """

        self.word2vec_model  = word2vec.w2v_model(self.config)

        self.word2vec_model.load_model()

    def voca_check(self,sentence,dictionary):
        """
            1. tokenized_sentence   :  given sentences would be tokenized.
                * What is your name -> ['What','is','your','name']

            2. without_stopwords    :  stop words in given sentences would be removed.
                * To play the basketball. -> ['play','baksetball']

            3. possible_blank_pos   :  possible blank position would be returned in list format.
                * [1,2,7] means that first element, second element and seventh element in
                'tokenized_sentence' are proper to be the blank. It is based on the basic word_list.
        """

        self.tokenized_sentence,self.without_stopwords,self.possible_blank_pos = self.nlp.possible_blank_position(sentence,dictionary)

    def generate_semantic_choices(self):
        """
            return value : dictionary with

                key   : possible position
                value : similar words

                ex) { 1 : ['apple','banna','peach'], 2 : ['computer','cell-phone','laptop']}

        """
        semantic_choices = {}
        delete_pos = []

        for pos in self.possible_blank_pos:

            # To reflect the semantics of context, those words around the target word would be set of input.
            n_gram_words = [] #
            for i in range(pos-3,pos+3):
                word = self.without_stopwords[i%len(self.without_stopwords)]
                n_gram_words.append(word)

            #get similar words. (arg1. positive) (arg2. negative) (arg3. option : word-only, --)
            result = self.word2vec_model.get_simliar_words(n_gram_words,[],"word-only")

            # differnt pos words would be removed.
            result = self.nlp.get_same_pos_words(result,self.tokenized_sentence[pos],self.word_dictionary)

            if(len(result) > 0):
                if (len(result) < self.config.number_of_result_choices):
                    delete_pos.append(pos)
                else:
                    semantic_choices[pos] = random.sample(result,self.config.number_of_result_choices)

        self.semantic_choices   = semantic_choices
        self.possible_blank_pos = self.update_list(self.possible_blank_pos,delete_pos,"delete")

    def update_list(self,target,update_contents,type):

        result = target
        if(type == "delte"):
            for element in update_contents:
                result.remove(element)
        return result

    def generate_sound_choices(self):
       """
       빈칸의 단어와 소리 유사도가 높은 오답 선지를 관련성이 큰 순서대로 6개를 도출
       """

       editex = sm.Editex()
       sound_choices = {}

       for pos in self.possible_blank_pos:

           similarity_list = []
           similarity_list2 = []

           for word in self.word_dictionary:
               if(self.tokenized_sentence[pos] != word):
                   similarity = (editex.get_sim_score(self.tokenized_sentence[pos], word) + jf.jaro_distance(self.tokenized_sentence[pos], word))/2
                   similarity_list.append([word, similarity])

           #print(similarity_list)
           similarity_list.sort(key = lambda x:x[1], reverse = True)
           #print("word is", self.tokenized_sentence[pos])

           for w in similarity_list[:self.config.number_of_result_choices]:
               similarity_list2.append(w[0])
           #print(random.sample(similarity_list[:6], 2))

           sound_choices[pos] = similarity_list2
           self.sound_choices = sound_choices
           #self.choices_of_words = choices_of_words
       #print(choices_of_words)

    def save_phonetic_matching(self):

        editex = sm.Editex()

        similarity_list = {}

        for word in self.word_dictionary:
            temp_list = []
            for compared_word in self.word_dictionary   :
                if(word == compared_word):
                    continue
                similarity = (editex.get_sim_score(word, compared_word) + jf.jaro_distance(word,compared_word))/2
                temp_list.append((compared_word,similarity))
            similarity_list[word] = temp_list

        for word in similarity_list:
            new = sorted(similarity_list[word], key=lambda x: x[1],reverse=True)
            similarity_list[word] = new

        f = open(self.config.phonetic_matching,"w")
        for word in similarity_list:
            output_string = word
            for compared_word in similarity_list[word]:
                output_string += " " + compared_word[0]
            f.write(output_string+"\n")
        f.close()

    def choices_intersection(self):
        """
            result value is choices_result with..

                key   : pssible_pos
                value : choices that is intersected with semantic_choices and sound_choices

                ex) { 1 : ['apple','banna','peach'], 2 : ['computer','cell-phone','laptop']}

            The ratio of arg of semantic_choices and sound_choices is randomly set.

        """
        choices_result = {}

        for possible_pos in self.possible_blank_pos:

            #temporary list to place variable choices.
            choice_list = []
            temp_dic    = {}

            if(possible_pos in self.semantic_choices.keys()):

                random_num = random.randrange(1,self.config.number_of_result_choices-1)
                remainder  = self.config.number_of_result_choices - random_num -1

                choice_list += (random.sample(self.semantic_choices[possible_pos],random_num))
                choice_list += (random.sample(self.sound_choices[possible_pos],remainder))

            # if there is no semantic choices then choices would be made of sound_choces only.
            else:

                choice_list += (random.sample(self.sound_choices[possible_pos],self.config.number_of_result_choices))

            #put choices made from above process into the choices_result dictionary.
            temp_dic['incorrect'] = list(set(choice_list))
            temp_dic['correct']   = self.tokenized_sentence[possible_pos]
            choices_result[possible_pos] = temp_dic

        self.choices_result = choices_result

    def project_problem_set(self):

        result_value = {}

        blank = self.config.word_blank

        # f = open(self.config.output_path,"w")
        idx = 0
        for pos in self.possible_blank_pos:
            temp = {}
            # rejoin the sentences with targeted blank
            output_sentence = list(self.tokenized_sentence)
            output_sentence[pos] = blank
            output_sentence = " ".join(output_sentence)

            # choices numbering
            choices = self.choices_result[pos]["incorrect"]
            answer  = self.choices_result[pos]["correct"]
            output_choices = {}

            for i in range(len(choices)):
                output_choices[i] = choices[i]

            temp["problem"] = output_sentence
            temp["choices"] = output_choices
            temp["answer"]  = answer

            result_value[idx] = temp

            idx += 1

        return result_value
        # f.close()
