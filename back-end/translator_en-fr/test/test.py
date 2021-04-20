import os
import tarfile
from transformers import MarianTokenizer, MarianMTModel

class Translator:
	def __init__(self):
		self.src = 'en'
		self.trg = 'fr'
		self.mname = f'Helsinki-NLP/opus-mt-{self.src}-{self.trg}'

		self.tokenizer = MarianTokenizer.from_pretrained(self.mname)
		self.model = MarianMTModel.from_pretrained(self.mname)

	def encode(self, text):
		return self.tokenizer.encode(text, return_tensors='pt')

	def decode(self, translation):
		return self.tokenizer.batch_decode(translation, skip_special_tokens=True)

	def predict(self, text):
		tokenized_text = self.encode(text)
		translation = self.model.generate(tokenized_text)
		print(translation)
		translated_text = self.decode(translation)[0]
		return translated_text



sentence = 'hello'
print(Translator().predict(sentence))


# Define name of directory to save pretrained model
path = './model'

if not os.path.exists(path):
	os.mkdir(path)

Translator().model.save_pretrained(path)
Translator().tokenizer.save_pretrained(path)

tar_name = 'marian-model-en-fr'
files = [files for root, dirs, files in os.walk(path)][0]
with tarfile.open(tar_name+ '.tar.gz', 'w:gz') as f:
	for root, dirs, files in os.walk(path):
		for file in files:
			f.add(os.path.join(root, file))
