from model import ngramModel
import save
import os
import glob

class userInterface:
    def __init__(self):
        # Initialization of the user interface
        pass

    def startInterface(self,model=None):
        # Start the user interface
        while True:
            inputInt = int(input("[1] Load training Data\n[2] Generate Text\n[3] Save model (Currently requires large amount of RAM with larger models)\n[4] Load model\n[5] Add dataset\n[6] Exit\n1-6: "))
            if inputInt == 1:
                try:
                    filepath = input("Filepath of unformatted Text: ")
                    n = int(input("Value for N: "))
                    model = ngramModel(n=n)
                    if os.path.isdir(filepath):
                        # If a directory is specified, iterate through all files in the directory and add them to the model
                        if filepath[-1] != "/":
                            # Ensure the filepath ends with a "/"
                            filepath += "/"
                        for file in glob.glob(filepath+"*"):
                            print(filepath+"/"+file)
                            model.addDataSet(file)
                    else:
                        # If a single file is specified, add it to the model
                        model.addDataSet(filepath)
                    print("Model has been trained")
                except ValueError:
                    # If N is not a valid integer print an error message
                    print("Invalid value for N")
                except FileNotFoundError:
                    # If the file is not found print an error message
                    print("File not found")
            elif inputInt == 2:
                if model != None: # Ensure that a model has been trained or loaded before generating text
                    contextString = input("Preceeding text: ")
                    textSize = input("Sentence amount: ")
                    if textSize == "":
                        # If no value is specified, default to 1
                        textSize = 1
                    else:
                        textSize = int(textSize)
                    generatedText = model.generateAmountOfSentences(textSeed=contextString,sentNum=textSize) # Generate the specified amount of sentences with the given context string
                    result = ""

                    # Print the generated text without brackets
                    for sentence in generatedText:
                        for word in sentence:
                            result += word + " "
                    print(contextString + result)
                else:
                    print("No model has been trained or loaded")
            elif inputInt == 3:
                if model != None: # Ensure that a model has been trained or loaded before saving
                    filepath = input("Save filepath: ")
                    save.saveModel(model=model,filepath=filepath) # Save the model to the specified filepath unsing the save module
                    print("Model has been saved")
                else:
                    print("No model has been trained or loaded")
            elif inputInt == 4:
                try: # Try to load a model from the specified filepath
                    filepath = input("Load filepath: ")
                    model = save.loadModel(filepath=filepath)
                    print("Model has been loaded")
                except FileNotFoundError: # If the file is not found print an error message
                    print("File not found")
            elif inputInt == 5:
                try: # Try to add a dataset to the existing model
                    filepath = input("Filepath of unformatted Text: ")
                    if os.path.isdir(filepath):
                        # If a directory is specified, iterate through all files in the directory and add them to the model
                        if filepath[-1] != "/":
                            # Ensure the filepath ends with a "/"
                            filepath += "/"
                        for file in glob.glob(filepath+"*"):
                            print(filepath+"/"+file)
                            model.addDataSet(file)
                    else:
                        # If a single file is specified, add it to the model
                        model.addDataSet(filepath)
                    print("Model has been trained")
                except FileNotFoundError:
                    # If the file is not found print an error message
                    print("File not found")
            elif inputInt == 6:
                break
            else:
                print("Invalid input")