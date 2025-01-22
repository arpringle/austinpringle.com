import os
import json
import textwrap
from jinja2 import Template

script_dir = os.path.dirname(os.path.realpath(__file__))

# Open the site description file
file = open(os.path.join(script_dir, "site-desc.json"), "r")
data = json.load(file)

# Parse the project tags and add links to the technology-specific pages to index.html
project_tags = data["project-tags"]

skill_grid_template = Template(open(os.path.join(script_dir, "./templates/skill-grid-item.html"), "r").read())

skill_grid_html_string = ""

index_template = Template(open(os.path.join(script_dir, "./templates/index.html"), "r").read())

for tag in project_tags:
    result = skill_grid_template.render(project_tag=tag["id"],tag_name_nice=tag["name-nice"])
    skill_grid_html_string = skill_grid_html_string + result

skill_grid_html_string = textwrap.indent(skill_grid_html_string, "                    ")

index_html = open("../index.html", "w")
index_html.write(index_template.render(skill_grid_items=skill_grid_html_string))

# Create the technology-specific pages
skill_page_template = Template(open(os.path.join(script_dir, "./templates/skill-page.html"), "r").read())

for tag in project_tags:
    skill_page_html = open(os.path.join(script_dir, "../projects/" + tag["id"] + ".html"), "w")
    skill_page_html.write(skill_page_template.render(technology_name=tag["name-nice"]))