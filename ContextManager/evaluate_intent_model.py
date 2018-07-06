from rasa_nlu.model import Metadata, Interpreter
from rasa_nlu.training_data import load_data
from rasa_nlu import evaluate
from sklearn import preprocessing
from sklearn.metrics import f1_score

model_location = '/Users/guolei/Documents/EIT/GUOLEI/ContextManager/projects/default/model_20180706-113329'

data_set = '/Users/guolei/Documents/EIT/GUOLEI/ContextManager/data/rasa_testing_15066_1525095686936.json'

testing_data = load_data(data_set)




def test_intent():
    #load model
    interpreter = Interpreter.load(model_location)
    # get true target of the testing data
    targets = evaluate.get_intent_targets(testing_data)
    # get predictions of the testing data
    predictions = evaluate.get_intent_predictions(interpreter, testing_data)
    #create a confusion matrix and summary statistics for intent predictions
    evaluate.evaluate_intents(targets,predictions)

    #generate classification report, precision, f1 score and accuary
    report, precision, f1, accuracy = evaluate.get_evaluation_metrics(targets, predictions)
    print("F1-Score:  {}\n".format(f1),
          "Precision: {}\n".format(precision),
          "Accuracy:  {}\n".format(accuracy),
          "Classification report: \n{}".format(report))

if  __name__ == '__main__':
    test_intent()