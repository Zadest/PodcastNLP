from textblob_de import TextBlobDE
import matplotlib.pyplot as plt

def showSentiment(text:str):
    blob = TextBlobDE(text)
    
    polarity = []
    for sentence in blob.sentences:
        if sentence.sentiment.subjectivity > 0.0 or sentence.sentiment.subjectivity < 0.0:
            polarity.append(sentence.sentiment.polarity)

    bar = [i for i in range(len(polarity))]
    
    fig = plt.figure(figsize = (10, 5))

    plt.bar(bar, polarity)
    plt.ylabel("Sentiment")
    plt.xlabel(range(0,len(blob.sentences)-1))
    plt.title("Polarity")
    plt.show()