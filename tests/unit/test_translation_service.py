# services/translation_service.py のテスト
import pytest
from app.services.translation_service import GoogleTranslator

@pytest.fixture(autouse=True)
def setup():
    trans = GoogleTranslator()
    yield trans

class TestTranslator():
    # 正常処理
    @pytest.mark.parametrize("origin_language, target_language, text, expected", [
        ("英語", "日本語", "Hello", "こんにちは"),
        ("日本語", "英語", "ありがとう", "thank you"), 
        ("フランス語", "ドイツ語", "Bonjour", "Guten Morgen"),
        ("日本語", "ドイツ語", "今は10時です", "Es ist jetzt 10 Uhr"),
    ])
    def test_convert_safe(self, setup, origin_language, target_language, text, expected):
        result = setup.convert(text, origin_language, target_language)
        print(result)
        assert result == expected
    
    # 例外処理
    @pytest.mark.parametrize("origin_language, target_language, text, expected", [
        ("アラビア語", "日本語", "こんにちは", None),  # 辞書に登録されていない言語
        ("日本語", "ドイツ語", "", None),  # textが空欄
        ("日本語", "", "こんにちは", None),  # target_languageが空欄
        ("", "英語", "こんにちは", None)  # origin_languageが空欄
    ])
    def test_convert_error(self, setup, origin_language, target_language, text, expected):
        result = setup.convert(text, origin_language, target_language)
        assert result == expected
