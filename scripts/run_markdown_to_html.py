from markdown_to_html import MarkdownToHTML

input_file = "../papers/camera_ready/SLw9fp4yI6/paper.md"
output_file = "../papers/camera_ready/SLw9fp4yI6/paper.html"

converter = MarkdownToHTML(input_file, output_file)
converter.convert_and_save()
