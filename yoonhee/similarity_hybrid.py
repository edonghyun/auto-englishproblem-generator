import py_stringmatching as sm
import jellyfish as jf

def similarity_hybrid(word1):
    dic = open('./voca_list/voca_all_sorted.txt', 'r')
    dic_line = dic.readlines()

    #종류가 다양
    #affine = sm.Affine()
    #bag_distance = sm.BagDistance()
    #needleman_wunsch = sm.NeedlemanWunsch()
    #partial_ratio = sm.PartialRatio()
    #partial_token_sort = sm.partial_token_sort()
    #ratio = sm.Ratio()
    #smith_waterman = sm.SmithWaterman()
    # token_sort = sm.TokenSort()
    #generalized_jaccard = sm.GeneralizedJaccard()
    #monge_elkan = sm.MongeElkan()
    # soft_tfidf = sm.SoftTfidf()

    editex = sm.Editex()

    similarity_list = []

    for line in dic_line:
        splited_line = line.split()
        word2 = splited_line[0].lower()

        if(word1 != word2):
            # similarity = affine.get_sim_score(word1, word2)
            #similarity = bag_distance.get_sim_score(word1, word2)
            #similarity = needleman_wunsch.get_sim_score(word1, word2)
            #similarity = partial_ratio.get_sim_score(word1, word2)
            #similarity = partial_token_sort.get_sim_score(word1, word2)
            #similarity = ratio.get_sim_score(word1, word2)
            #similarity = smith_waterman.get_sim_score(word1, word2)
            # similarity = token_sort.get_sim_score(word1, word2)
            #similarity = generalized_jaccard.get_sim_score(word1, word2)
            #similarity = monge_elkan.get_sim_score(word1, word2)
            # similarity = soft_tfidf.get_sim_score(word1, word2)
            similarity = (editex.get_sim_score(word1, word2) + jf.jaro_distance(word1, word2))/2
            similarity_list.append([word2, similarity])

    #print(similarity_list)
    similarity_list.sort(key = lambda x:x[1], reverse = True)

    for w in similarity_list[:10]:
        print(w[0])

if __name__ == '__main__':

    words = ['distinction', 'extinction', 'extension', 'detention', 'excision',
    'effort', 'effect', 'affection', 'affectation',
    'custody', 'custom', 'fare', 'fee', 'accord', 'discord',
    'record', 'accordingly', 'according',
    'dedication', 'decadent', 'acclimatize', 'accomodate']

    for word in words:
        print("Word is ", word)
        similarity_hybrid(word)
        print("\n")
