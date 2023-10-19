from flask import request, render_template, jsonify
from . import application
import json
from app.evaluation_metrics import evaluation

@application.route('/', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':

        f1 = request.files['file1']
        f1.save(f1.filename)
        ff1 = open(f1.filename, 'r')

        f2 = request.files['file2']
        f2.save(f2.filename)
        ff2 = open(f2.filename, 'r')

        content1 = json.load(ff1)
        content2 = json.load(ff2)

        eval_metric = evaluation()

        # Kappa
        all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval_metric.matching_calculation(
            content1, content2)
        kappa = eval_metric.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,
                                       prop_ya_cm)

        # CASS
        text_similarity = eval_metric.text_similarity(content1, content2)
        # CASS
        cass = eval_metric.CASS_calculation(text_similarity, kappa)

        # F1
        f1 = eval_metric.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,prop_ya_cm)


        # Accuracy
        acc = eval_metric.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,prop_ya_cm)


        # Gamma
        gamma = eval_metric.gamma_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)


        # U-Alpha
        u_alpha = eval_metric.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,prop_ya_cm)

        # result
        results = {
            "Macro F1": f1,
            "Accuracy": acc,
            "CASS": cass,
            "Text Similarity":text_similarity,
            "U-Alpha": u_alpha,
            "Gamma": gamma,
            "Kappa": kappa
          }

        return jsonify(results)

    elif request.method == 'GET':
        return render_template('docs.html')
