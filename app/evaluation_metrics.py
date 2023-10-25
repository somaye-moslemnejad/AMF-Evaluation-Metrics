from app.matching import match
import json
from pycm import *
class evaluation:


    @staticmethod
    def matching_calculation(data1, data2):
        json1 = data1['AIF']
        json2 = data2['AIF']
        # Graph construction
        graph1,graph2= match.get_graphs(json1, json2)
        # creating proposition similarity matrix relations
        prop_rels = match.get_prop_sim_matrix(graph1, graph2)
        # creating locution similarity matrix relations
        loc_rels = match.get_loc_sim_matrix(graph1, graph2)
        # anchoring on s-nodes (RA/CA/MA) and combining them
        ra_a = match.ra_anchor(graph1, graph2)
        ma_a = match.ma_anchor(graph1, graph2)
        ca_a = match.ca_anchor(graph1, graph2)
        all_a = match.combine_s_node_matrix(ra_a, ca_a, ma_a)
        all_s_a_dict = match.convert_to_dict(all_a)
        # propositional relation comparison
        prop_rels_comp_conf = match.prop_rels_comp(prop_rels,graph1, graph2)
        prop_rels_comp_dict = match.convert_to_dict(prop_rels_comp_conf)
       # getting all YAs anchored in Locutions
        loc_ya_rels_comp_conf = match.loc_ya_rels_comp(loc_rels, graph1, graph2)
        loc_ya_rels_comp_dict = match.convert_to_dict(loc_ya_rels_comp_conf)
        # getting all YAs in propositions
        prop_ya_comp_conf = match.prop_ya_comp(prop_rels, graph1, graph2)
        prop_ya_comp_dict = match.convert_to_dict(prop_ya_comp_conf)
        # getting all TAs anchored in Locutions
        loc_ta_conf = match.loc_ta_rels_comp(loc_rels, graph1, graph2)
        loc_ta_dict = match.convert_to_dict(loc_ta_conf)
        # getting all YAs anchored in propositions
        prop_ya_conf = match.prop_ya_anchor_comp(prop_rels, graph1, graph2)
        prop_ya_dict = match.convert_to_dict(prop_ya_conf)




        # creating confusion matrix for s-nodes/YA/TA
        all_s_a_cm = ConfusionMatrix(matrix=all_s_a_dict)
        prop_rels_comp_cm = ConfusionMatrix(matrix=prop_rels_comp_dict)
        loc_ya_rels_comp_cm = ConfusionMatrix(matrix=loc_ya_rels_comp_dict)
        prop_ya_comp_cm = ConfusionMatrix(matrix=prop_ya_comp_dict)
        loc_ta_cm = ConfusionMatrix(matrix=loc_ta_dict)
        prop_ya_cm = ConfusionMatrix(matrix=prop_ya_dict)

        return all_s_a_cm,prop_rels_comp_cm,loc_ya_rels_comp_cm,prop_ya_comp_cm,loc_ta_cm,prop_ya_cm



    # Kappa range from -1 to +1
    @staticmethod
    def kappa_calculation(all_s_a_cm,prop_rels_comp_cm,loc_ya_rels_comp_cm,prop_ya_comp_cm,loc_ta_cm,prop_ya_cm):
        # kappa calculation
        s_node_kapp = all_s_a_cm.Kappa
        prop_rel_kapp = prop_rels_comp_cm.Kappa
        loc_rel_kapp = loc_ya_rels_comp_cm.Kappa
        prop_ya_kapp = prop_ya_comp_cm.Kappa
        loc_ta_kapp = loc_ta_cm.Kappa
        prop_ya_an_kapp = prop_ya_cm.Kappa


        if match.check_none(s_node_kapp):
            s_node_kapp = all_s_a_cm.KappaNoPrevalence
        if match.check_none(prop_rel_kapp):
            prop_rel_kapp = prop_rels_comp_cm.KappaNoPrevalence
        if match.check_none(loc_rel_kapp):
            loc_rel_kapp = loc_ya_rels_comp_cm.KappaNoPrevalence
        if match.check_none(prop_ya_kapp):
            prop_ya_kapp = prop_ya_comp_cm.KappaNoPrevalence
        if match.check_none(loc_ta_kapp):
            loc_ta_kapp = loc_ta_cm.KappaNoPrevalence
        if match.check_none(prop_ya_an_kapp):
            prop_ya_an_kapp = prop_ya_cm.KappaNoPrevalence


        score_list = [s_node_kapp, prop_rel_kapp, loc_rel_kapp, prop_ya_kapp, loc_ta_kapp, prop_ya_an_kapp]
        k_graph = sum(score_list) / float(len(score_list))

        return k_graph
        # CASS calculation

    @staticmethod
    def text_similarity(data1, data2):
        text1 = data1['text']
        text2 = data2['text']
        # Similarity between two texts
        ss = match.get_similarity(text1, text2)
        if ss == 'Error Text Input Is Empty' or ss == 'None:Error! Source Text Was Different as Segmentations differ in length':
            return ss
        else:
         return ss

    @staticmethod
    def CASS_calculation(text_sim_ss,k_graph):
            if text_sim_ss == 'Error Text Input Is Empty' or text_sim_ss == 'None:Error! Source Text Was Different as Segmentations differ in length':
                overall_sim='None'
            else:

             overall_sim = (k_graph + text_sim_ss) / 2

            return overall_sim


    # f1 0-1
    @staticmethod
    def F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm):
        # Get F1 macro scores from confusion matrices for each category/class
        s_node_F1_macro = all_s_a_cm.F1_Macro
        prop_rel_F1_macro = prop_rels_comp_cm.F1_Macro
        loc_rel_F1_macro = loc_ya_rels_comp_cm.F1_Macro
        prop_ya_F1_macro = prop_ya_comp_cm.F1_Macro
        loc_ta_F1_macro = loc_ta_cm.F1_Macro
        prop_ya_an_F1_macro = prop_ya_cm.F1_Macro

        if match.check_none(s_node_F1_macro):
            s_node_F1_macro = 1.0
        if match.check_none(prop_rel_F1_macro):
            prop_rel_F1_macro = 1.0
        if match.check_none(loc_rel_F1_macro):
            loc_rel_F1_macro = 1.0
        if match.check_none(prop_ya_F1_macro):
            prop_ya_F1_macro = 1.0
        if match.check_none(loc_ta_F1_macro):
            loc_ta_F1_macro = 1.0
        if match.check_none(prop_ya_an_F1_macro):
            prop_ya_an_F1_macro = 1.0
        score_list = [s_node_F1_macro, prop_rel_F1_macro, loc_rel_F1_macro, prop_ya_F1_macro, loc_ta_F1_macro, prop_ya_an_F1_macro]

        F1_macro = sum(score_list) / float(len(score_list))

        return F1_macro
    #  accuracy 0-1
    @staticmethod
    def accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,
                             prop_ya_cm):
        # Get accuracy scores from confusion matrices for each category/class
        s_node_accuracy = all_s_a_cm.ACC
        prop_rel_accuracy = prop_rels_comp_cm.ACC
        loc_rel_accuracy = loc_ya_rels_comp_cm.ACC
        prop_ya_accuracy = prop_ya_comp_cm.ACC
        loc_ta_accuracy = loc_ta_cm.ACC
        prop_ya_an_accuracy = prop_ya_cm.ACC


        # Handle cases where accuracy is None
        def handle_accuracy(acc_dict):
            acc_dict = {k: v if v is not None else 1 for k, v in acc_dict.items()}
            return acc_dict

        s_node_accuracy = handle_accuracy(s_node_accuracy)
        prop_rel_accuracy = handle_accuracy(prop_rel_accuracy)
        loc_rel_accuracy = handle_accuracy(loc_rel_accuracy)
        prop_ya_accuracy = handle_accuracy(prop_ya_accuracy)
        loc_ta_accuracy = handle_accuracy(loc_ta_accuracy)
        prop_ya_an_accuracy = handle_accuracy(prop_ya_an_accuracy)

        # Calculate the average accuracy for each class
        def calculate_average_accuracy(acc_dict):
            values = list(acc_dict.values())
            return sum(values) / len(values) if len(values) > 0 else 0

        s_node_accuracy = calculate_average_accuracy(s_node_accuracy)
        prop_rel_accuracy = calculate_average_accuracy(prop_rel_accuracy)
        loc_rel_accuracy = calculate_average_accuracy(loc_rel_accuracy)
        prop_ya_accuracy = calculate_average_accuracy(prop_ya_accuracy)
        loc_ta_accuracy = calculate_average_accuracy(loc_ta_accuracy)
        prop_ya_an_accuracy = calculate_average_accuracy(prop_ya_an_accuracy)


        score_list = [s_node_accuracy, prop_rel_accuracy, loc_rel_accuracy, prop_ya_accuracy, loc_ta_accuracy,
                      prop_ya_an_accuracy]

        Accuracy = sum(score_list) / float(len(score_list))

        return Accuracy

    # U-Alpha range from 0 to 1
    @staticmethod
    def u_alpha_calculation(all_s_a_cm,prop_rels_comp_cm,loc_ya_rels_comp_cm,prop_ya_comp_cm,loc_ta_cm,prop_ya_cm):
        # u-alpha calculation
        s_node_u_alpha = all_s_a_cm.Alpha
        prop_rel_u_alpha = prop_rels_comp_cm.Alpha
        loc_rel_u_alpha = loc_ya_rels_comp_cm.Alpha
        prop_ya_u_alpha = prop_ya_comp_cm.Alpha
        loc_ta_u_alpha = loc_ta_cm.Alpha
        prop_ya_an_u_alpha = prop_ya_cm.Alpha


        if match.check_none(s_node_u_alpha):
            s_node_u_alpha = 1.0
        if match.check_none(prop_rel_u_alpha):
            prop_rel_u_alpha = 1.0
        if match.check_none(loc_rel_u_alpha):
            loc_rel_u_alpha  = 1.0
        if match.check_none(prop_ya_u_alpha):
            prop_ya_u_alpha = 1.0
        if match.check_none(loc_ta_u_alpha):
            loc_ta_u_alpha = 1.0
        if match.check_none(prop_ya_an_u_alpha):
            prop_ya_an_u_alpha = 1.0


        score_list = [s_node_u_alpha, prop_rel_u_alpha, loc_rel_u_alpha, prop_ya_u_alpha, loc_ta_u_alpha, prop_ya_an_u_alpha]
        u_alpha = sum(score_list) / float(len(score_list))

        return u_alpha

    # Gamma based on https://www.pycm.io/doc/index.html /https://aclanthology.org/J15-3003.pdf/https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61/https://nces.ed.gov/FCSM/pdf/J4_Xie_2013FCSM.pdf
    @staticmethod
    def gamma_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,
                              prop_ya_cm):
            # kappa calculation
            s_node_gamma = all_s_a_cm.AC1
            prop_rel_gamma = prop_rels_comp_cm.AC1
            loc_rel_gamma = loc_ya_rels_comp_cm.AC1
            prop_ya_gamma = prop_ya_comp_cm.AC1
            loc_ta_gamma = loc_ta_cm.AC1
            prop_ya_an_gamma = prop_ya_cm.AC1

            if match.check_none(s_node_gamma):
                s_node_gamma = 1.0
            if match.check_none(prop_rel_gamma):
                prop_rel_gamma = 1.0
            if match.check_none(loc_rel_gamma):
                loc_rel_gamma = 1.0
            if match.check_none(prop_ya_gamma):
                prop_ya_gamma = 1.0
            if match.check_none(loc_ta_gamma):
                loc_ta_gamma = 1.0
            if match.check_none(prop_ya_an_gamma):
                prop_ya_an_gamma = 1.0

            score_list = [s_node_gamma, prop_rel_gamma, loc_rel_gamma, prop_ya_gamma, loc_ta_gamma, prop_ya_an_gamma]
            gamma = sum(score_list) / float(len(score_list))

            return gamma

# Debugging

if __name__ == "__main__":
        eval=evaluation()
        file1 = open('../28037.json', 'r')
        data1 = json.load(file1)
        file2 = open('../28111.json', 'r')
        data2 = json.load(file2)
        # Kappa
        all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm=eval.matching_calculation(data1,data2)

        kappa=eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
        print('kappa',kappa)

        # Text Similarity and CASS
        Text_similarity=eval.text_similarity(data1,data2)
        print('text similarity',Text_similarity)

        CASS = eval.CASS_calculation(Text_similarity, kappa)
        print('CASS',CASS)


        # F1
        F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
        print('F1', F1)
        # accuracy
        Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,
                                  prop_ya_cm)
        print('Accuracy', Acc)

        # U-Alpha
        U_Alpha= eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,
                                   prop_ya_cm)
        print('U-Alpha', U_Alpha)

        # Gamma
        Gamma = eval.gamma_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                           loc_ta_cm,
                                           prop_ya_cm)
        print('Gamma', Gamma)





