from rasa_nlu.model import Interpreter
from rasa_nlu.training_data import load_data
from rasa_nlu import evaluate
from collections import defaultdict

model_location = '/Users/guolei/Documents/EIT/GUOLEI/ContextManager/projects/default/model_20180706-113329'

data_set = '/Users/guolei/Documents/EIT/GUOLEI/ContextManager/data/rasa_testing_15066_1525095686936.json'

testing_data = load_data(data_set)

def test_entity():
    #load model
    interpreter = Interpreter.load(model_location)

    duckling_extractors = {"ner_duckling", "ner_duckling_http"}

    #create dictionary of entity results
    entity_results = defaultdict(lambda: defaultdict(list))

    #get extractors of the interpreter
    extractors = evaluate.get_entity_extractors(interpreter)

    #get entity predictions and tokens
    entity_predictions, tokens = evaluate.get_entity_predictions(interpreter, testing_data)

    # Create classification report
    if duckling_extractors.intersection(extractors):
        entity_predictions = evaluate.remove_duckling_entities(entity_predictions)
        extractors = evaluate.remove_duckling_extractors(extractors)

    if not extractors:
        return entity_results

    #get entity_targets
    entity_targets = evaluate.get_entity_targets(testing_data)

    #get aligned_prections
    aligned_predictions = evaluate.align_all_entity_predictions(entity_targets,
                                                                entity_predictions,
                                                                tokens, extractors)

    merged_targets = evaluate.merge_labels(aligned_predictions)
    merged_targets = evaluate.substitute_labels(merged_targets, "O", "no_entity")

    for extractor in extractors:
        merged_predictions = evaluate.merge_labels(aligned_predictions, extractor)
        merged_predictions = evaluate.substitute_labels(merged_predictions, "O",
                                                        "no_entity")
        report, precision, f1, accuracy = evaluate.get_evaluation_metrics(merged_targets,
                                                                          merged_predictions)
        entity_results[extractor]["Accuracy"].append(accuracy)
        entity_results[extractor]["F1-score"].append(f1)
        entity_results[extractor]["Precision"].append(precision)

    print("entity_results:  {}\n".format(entity_results),
          "Classification report: \n{}".format(report))


if __name__ =='main':
    test_entity()