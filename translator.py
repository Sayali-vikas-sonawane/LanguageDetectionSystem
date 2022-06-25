from googletrans import Translator
#translator = google_translator()
translator = Translator()
text = "my name"
translate_text = translator.translate(text, dest='hi')
print(translate_text)