from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

model_name = "oliverguhr/spelling-correction-english-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def correct_spelling_and_grammar(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=128, truncation=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=128, num_beams=5, early_stopping=True)
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_text


input_text = "tun on the lghts i te kichen"
corrected = correct_spelling_and_grammar(input_text)
print("🔸 Input:", input_text)
print("✅ Final Correction:", corrected)