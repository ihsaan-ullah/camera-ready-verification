import markdown


class MarkdownToHTML:

    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def convert_and_save(self):
        with open(self.input_file_path, "r", encoding="utf-8") as f:
            text = f.read()

        html = markdown.markdown(text)

        with open(self.output_file_path, "w", encoding="utf-8") as f:
            f.write(html)
