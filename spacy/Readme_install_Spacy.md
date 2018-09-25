## downlaod language module from:
https://spacy.io/usage/models#download-pip

## pip install model 
pip install /Users/you/en_core_web_md-1.2.1.tar.gz

# you can also use external ur
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-1.2.1/en_core_web_md-1.2.1.tar.gz

#you may need to create a shortcut link
https://spacy.io/usage/models#usage-link


## in you python environment 
import en_core_web_md
nlp = en_core_web_sm.load()
doc = nlp('this is a sentence')