# Scandinavian language classifier

## Environment

For development I used the anaconda environment manager.

```bash
conda create --name lan_wire python==3.7
conda activate lan_wire
pip install -r requirements.txt
```

## Data

As data source the danish, swedish and norwegian wikipedia was used. The texts were downloaded using their API.
A python wikipedia wrapper was used for easier use in python.
The data can be downloaded running the download_data.py script.

```bash
python download_data.py
```

You must specify the language code (da/sv/no) and the title of the topic for which the data should be downloaded. The title must be specified in the language you want to download for. For the training data the Politics and Nature title was used. For training the model 81000 data samples were used, which was divided into train and test set. The constructed vocabulary consisted of 164700 words. The more topics and data you download the bigger the vocalbulary will be, thus the more accurate predictions you will get. 

## Preprocessing

The data preprocessing is part of the preprocess.ipynb jupyter notebook.
The preprocessing steps taken:

1. New line signs were removed (\n)
2. The texts were divided into sentences
3. All the text was lowercased
4. All sentences were divided into words (To encode as embeddings)
5. Only alphanumeric characters were used

Removing stop words and stemming was also considered.

The data was divided into train and test set in ratio 80%/20%.

## Model development

The pytorch framework was used for model development.
A two layer LSTM network with three feed forward layers on the top was developed. Batchnorm and Dropout was used to avoid overfitting. ReLU was used as activation function between the layers and softmax after the last layer to distribute the probabilities across the labels.
A vocabulary was constructed from the train and test data in order to encode the input to numeric values.
A lookup table was constructed to get the indexes from the vocabulary. Embedding layer was used as first layer in the network.

## Training a model

The model was trained for 50 epochs with batch size 72 and learning rate 0.0005. Adam was used as optimization algorithm.
CrossEntropy was used as loss function. After each epoch a validation was performed, where the loss and the accuracy of the network was calculated. In every validation the accuracy is compared to the current best model and if it's more, the weights are saved.

The checkpoints of the models will are saved in

```bash
app/lang_model/data/models/{modelname}/{accuracy}_.pt.
```

More details can be find in the notebook modelling.py.
The highest accuracy achieved was 91.3 %. Of course, this can be further tuned, with improving the data, hyperparameter tuning and achitecture tuning.

## Rest API

The trained model is exposed via a REST API. The rest api was developed using the fastapi framework. The application runs on uvicorn.

To run the app:

```bash
cd app
uvicorn main:app --reload
```

The requests are accepted at url "/lang" and must contain a url parameter "text" with a text in ont of the three languages (danish, swedish or norwegian).
The return will contain the language of the text.

The implementation can be found in the app/lang_model folder, while the API is in the main.py file.

## Running from docker

The application was dockerized.
To build the container:

```bash
docker build -t lan_wire .
```

To run the app:

```bash
docker run -d --name lan_wire -p 80:80 lan_wire
```

The app will be served at "http://127.0.0.1/lang?text={yourtexttotranslate}"
