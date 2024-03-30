from docxtpl import DocxTemplate
import os


class TemplateProcessor:
    def __init__(self, template_path):
        self.template = DocxTemplate(template_path)

    def render_template(self, context):
        self.template.render(context)

    def save(self, output_path):
        self.template.save(output_path)


class DataValidator:
    def __init__(self, template_processor, dataset):
        self.template_processor = template_processor
        self.dataset = dataset

    def validate(self):
        template_vars = self.template_processor.template.get_undeclared_template_variables()
        missing_in_dataset = set(template_vars) - set(self.dataset.keys())
        missing_in_template = set(self.dataset.keys()) - set(template_vars)

        if missing_in_dataset:
            raise ValueError(f"Внимание: В шаблоне есть переменные, которых нет в dataset: {missing_in_dataset}")

        if missing_in_template:
            print(f"Внимание: В dataset есть данные, которых нет в шаблоне: {missing_in_template}")

        return True


class DocumentGenerator:
    def __init__(self, template_path, dataset, output_path):
        self.template_processor = TemplateProcessor(template_path)
        self.dataset = dataset
        self.output_path = output_path

    def generate(self):
        validator = DataValidator(self.template_processor, self.dataset)
        if validator.validate():
            self.template_processor.render_template(self.dataset)
            self.template_processor.save(self.output_path)
            print(f"Документ {os.path.basename(self.output_path)} успешно сгенерирован.")
        else:
            print("Документ не может быть сгенерирован из-за ошибок валидации.")


if __name__ == '__main__':
    dataset = {
        'table_contents': [
            {'slot_number': '001', 'spp_number': 'A01', 'spp_date': '2024-01-01', 'winner_name': 'Иванов И.И.',
             'payment_purpose': 'За услуги', 'payment_sum': 10000},
            # Другие строки таблицы
        ],
        'company_name': 'Компания ООО',
        'bill_number': '12345',
        # Другие данные
    }

    template_path = 'path_to_template.docx'
    output_path = 'output_document.docx'

    doc_gen = DocumentGenerator(template_path, dataset, output_path)
    doc_gen.generate()
