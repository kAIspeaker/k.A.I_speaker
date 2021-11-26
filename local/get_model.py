
# import torch
# from torch import nn
# import numpy as np
# import gluonnlp as nlp
# from kobert_tokenizer import KoBERTTokenizer
# from transformers import BertModel
# from torch.utils.data import Dataset, DataLoader


# class BERTDataset(Dataset):
# 	def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer,vocab, max_len,
# 				 pad, pair):
# 		transform = nlp.data.BERTSentenceTransform(bert_tokenizer,vocab=vocab,max_seq_length=max_len, pad=pad, pair=pair)

# 		self.sentences = [transform([i[sent_idx]]) for i in dataset]
# 		self.labels = [np.int32(i[label_idx]) for i in dataset]

# 	def __getitem__(self, i):
# 		return (self.sentences[i] + (self.labels[i], ))

# 	def __len__(self):
# 		return (len(self.labels))

# class BERTClassifier(nn.Module):
# 	def __init__(self,
# 				 bert,
# 				 hidden_size = 768,
# 				 num_classes=11,
# 				 dr_rate=None,
# 				 params=None):
# 		super(BERTClassifier, self).__init__()
# 		self.bert = bert
# 		self.dr_rate = dr_rate

# 		self.classifier = nn.Linear(hidden_size , num_classes)
# 		if dr_rate:
# 			self.dropout = nn.Dropout(p=dr_rate)

# 	def gen_attention_mask(self, token_ids, valid_length):
# 		attention_mask = torch.zeros_like(token_ids)
# 		for i, v in enumerate(valid_length):
# 			attention_mask[i][:v] = 1
# 		return attention_mask.float()

# 	def forward(self, token_ids, valid_length, segment_ids):
# 		attention_mask = self.gen_attention_mask(token_ids, valid_length)

# 		_, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device), return_dict=False)
# 		# _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device), return_dict=False)
# 		if self.dr_rate:
# 			out = self.dropout(pooler)
# 		return self.classifier(out)



# ## Setting parameters
# max_len = 64
# batch_size = 64
# warmup_ratio = 0.1
# num_epochs = 10
# max_grad_norm = 1
# log_interval = 200
# learning_rate =  5e-5

# def predict(predict_sentence, model, tok, vocab):

# 	data = [predict_sentence, '0']
# 	dataset_another = [data]

# 	another_test = BERTDataset(dataset_another, 0, 1, tok, vocab, max_len, True, False)
# 	test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=2)

# 	model.eval()

# 	for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
# 		token_ids = token_ids.long()
# 		segment_ids = segment_ids.long()
# 		valid_length= valid_length
# 		label = label.long()

# 		out = model(token_ids, valid_length, segment_ids)

# 		test_eval=[]
# 		for i in out:
# 			logits=i
# 			logits = logits.detach().cpu().numpy()

# 			if np.argmax(logits) == 0:
# 				test_eval.append("결제")
# 			elif np.argmax(logits) == 1:
# 				test_eval.append("메뉴판")
# 			elif np.argmax(logits) == 2:
# 				test_eval.append("변경")
# 			elif np.argmax(logits) == 3:
# 				test_eval.append("영수증")
# 			elif np.argmax(logits) == 4:
# 				test_eval.append("재고_확인")
# 			elif np.argmax(logits) == 5:
# 				test_eval.append("정보_가격")
# 			elif np.argmax(logits) == 6:
# 				test_eval.append("정보_메뉴")
# 			elif np.argmax(logits) == 7:
# 				test_eval.append("정보_제휴")
# 			elif np.argmax(logits) == 8:
# 				test_eval.append("주문")
# 			elif np.argmax(logits) == 9:
# 				test_eval.append("추천")
# 			elif np.argmax(logits) == 10:
# 				test_eval.append("포인트_적립")

		# return (test_eval[0])

# def get_model():
#   model = torch.load('./k_A_I_speaker.pt', map_location=torch.device('cpu'))
#   # bertmodel = BertModel.from_pretrained('skt/kobert-base-v1')
#   tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
#   vocab = tokenizer.vocab_file
#   vocab = nlp.vocab.BERTVocab.from_sentencepiece(vocab, padding_token='[PAD]')

#   tok = tokenizer.tokenize

#   return model, tok, vocab
