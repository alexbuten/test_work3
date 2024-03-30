import unittest
from TemplateEngine import TemplateProcessor, DataValidator, DocumentGenerator


class TestTemplateEngine(unittest.TestCase):
    def setUp(self):
        self.dataset = {
            'table_contents': [
                {'slot_number': '001', 'spp_number': 'A01', 'spp_date': '2024-01-01', 'winner_name': 'Иванов И.И.', 'payment_purpose': 'За услуги', 'payment_sum': 10000},
                # Другие строки таблицы
            ],
            'company_name': 'Компания ООО',
            'bill_number': '12345',
            # Другие данные
        }
        self.template_path = 'test_template.docx'  # Этот файл должен быть предварительно создан для тестирования
        self.output_path = 'test_output.docx'

    def test_validation_success(self):
        template_processor = TemplateProcessor(self.template_path)
        validator = DataValidator(template_processor, self.dataset)
        self.assertTrue(validator.validate(), "Валидация должна пройти успешно")

    def test_validation_failure(self):
        template_processor = TemplateProcessor(self.template_path)
        invalid_dataset = self.dataset.copy()
        del invalid_dataset['bill_number']  # Удаляем обязательный ключ для провала валидации
        validator = DataValidator(template_processor, invalid_dataset)
        with self.assertRaises(ValueError):
            validator.validate()

    def test_document_generation(self):
        doc_gen = DocumentGenerator(self.template_path, self.dataset, self.output_path)
        doc_gen.generate()
        self.assertTrue(os.path.exists(self.output_path), "Документ должен быть сгенерирован")


if __name__ == '__main__':
    unittest.main()
