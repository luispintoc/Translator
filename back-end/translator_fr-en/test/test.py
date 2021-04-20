from transformers import PretrainedConfig, AutoTokenizer, MarianMTModel, MarianTokenizer
import torch

model_path = './model'
config = PretrainedConfig.from_pretrained(f'{model_path}/model_config.json')
state = torch.load(f'{model_path}/Marian_pytorch_model_fr-en.bin')

src = 'fr'
trg = 'en'
mname = f'Helsinki-NLP/opus-mt-{src}-{trg}'
text = 'bonjour'

model = MarianMTModel.from_pretrained(
		pretrained_model_name_or_path=None, state_dict=state, config=config)

# src = 'en'
# trg = 'fr'
# mname = f'Helsinki-NLP/opus-mt-{src}-{trg}'
# text = 'hello'
# tokenizer = MarianTokenizer.from_pretrained(mname)#.save_pretrained('./model')
tokenizer = AutoTokenizer.from_pretrained('./model')#.save_pretrained('./model')
tokenized_text = tokenizer.encode(text, return_tensors='pt')
translation = model.generate(tokenized_text)
s = tokenizer.batch_decode(translation, skip_special_tokens=True)[0]
print(s)