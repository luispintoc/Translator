from transformers import PretrainedConfig, AutoTokenizer, MarianMTModel
import torch
import boto3
import json
import io

s3 = boto3.client('s3')

class TranslatorModel_fr_en:
	def __init__(self, model_path=None, s3_bucket=None,  model_prefix=None):
		self.model, self.tokenizer = self.from_pretrained(model_path, s3_bucket, model_prefix)

	def from_pretrained(self, model_path:str, s3_bucket: str, model_prefix:str):
		model = self.load_model_from_s3(model_path, s3_bucket, model_prefix)
		tokenizer = self.load_tokenizer(model_path)
		return model, tokenizer

	def load_model_from_s3(self, model_path:str, s3_bucket: str, model_prefix:str):
		if model_path and s3_bucket and model_prefix:
			obj = s3.get_object(Bucket=s3_bucket, Key=model_prefix)

			config = PretrainedConfig.from_pretrained(f'{model_path}/model_config.json')
			state = torch.load(io.BytesIO(obj['Body'].read()))

			model = MarianMTModel.from_pretrained(
					pretrained_model_name_or_path=None, state_dict=state, config=config)

			return model
		else:
			raise KeyError('Error loading model from s3')

	def load_tokenizer(self, model_path:str):
		tokenizer = AutoTokenizer.from_pretrained(model_path)
		return tokenizer

	def encode(self, text):
		return self.tokenizer.encode(text, return_tensors='pt')

	def decode(self, translation):
		return self.tokenizer.batch_decode(translation, skip_special_tokens=True)

	def predict(self, text):
		tokenized_text = self.encode(text)
		translation = self.model.generate(tokenized_text)
		translated_text = self.decode(translation)[0]
		return translated_text