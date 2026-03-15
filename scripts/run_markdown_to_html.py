from markdown_to_html import MarkdownToHTML


# input_file = "../papers/submitted/MbfAK4s61A_2308_06463v1/paper.md"
# output_file = "../papers/submitted/MbfAK4s61A_2308_06463v1/paper.html"

input_file = "../papers/camera_ready/MbfAK4s61A_2308_06463/paper.md"
output_file = "../papers/camera_ready/MbfAK4s61A_2308_06463/paper.html"

converter = MarkdownToHTML(input_file, output_file)
converter.convert_and_save()