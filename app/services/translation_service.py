# 翻訳機能の提供
from googletrans import Translator

class GoogleTranslator():
    def __init__(self):
        self.translator = Translator()
        self.languages = {
            '日本語': 'ja',
            '英語': 'en',
            '中国語': 'zh-cn',
            'フランス語': 'fr',
            'ドイツ語': 'de',
            'ヒンディー語': 'hi',
            'イタリア語': 'it',
            '韓国語': 'ko',
            'ロシア語': 'ru',
            'スペイン語': 'es',
        }
    
    def get_language_id(self, language_name):
        return self.languages.get(language_name, None)

    def convert(self, text_origin, get_language_id, trans_lang_name):
        if not text_origin:
            return None

        language_origin_id = self.get_language_id(get_language_id)
        language_translationed_id = self.get_language_id(trans_lang_name)
        if language_origin_id is None:
            return None

        if language_translationed_id is None:
            return None
            
        text_translationed = self.translator.translate(text_origin, src=language_origin_id, dest=language_translationed_id)
        return text_translationed.text