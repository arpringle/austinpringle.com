import os
import json
import textwrap
import shutil
from collections import defaultdict
from jinja2 import Template

# Set the working directory to be this folder (In case the user tries to execute it from a different
# directory; which would break the relative paths)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Clear and remake the public directory
if os.path.exists("./.public"):
    shutil.rmtree("./.public")
os.mkdir("./.public")
os.mkdir("./.public/projects")


# Open the site description file
site_description_file = open("./site-desc.json", "r")
site_description = json.load(site_description_file)

header_html_string = open("./templates/header.html").read()
header_html_string = textwrap.indent(header_html_string, "        ")

#
# Create the technology-specific tiles on index.html
#
project_tags = site_description["project-tags"]

skill_grid_template = Template(open("./templates/skill-grid-item.html", "r").read())

skill_grid_html_string = ""

index_template = Template(open("./templates/index.html", "r").read())

for tag in project_tags:
    tag_id = tag["id"]
    tag_name = tag["name-nice"]
    result = skill_grid_template.render(project_tag=tag_id, tag_name_nice=tag_name)
    skill_grid_html_string = skill_grid_html_string + result + "\n"

skill_grid_html_string = textwrap.indent(skill_grid_html_string, "                    ")

index_html = open("./.public/index.html", "w")
index_html.write(index_template.render(skill_grid_items=skill_grid_html_string, header=header_html_string))

#
# Create reusable project tiles to show on the various "skill" pages
#
tags_to_project_render_dict = defaultdict(list)

project_tile_template = Template(open("./templates/project-tile.html", "r").read())

projects = site_description["projects"]

project_tiles_concatenated = ""

for project in projects:
    project_tile_rendered = project_tile_template.render(project_id=project["id"], project_name=project["name-nice"])
    for tag in project["tags"]:
        tags_to_project_render_dict[tag].append(project_tile_rendered)
    project_tiles_concatenated += project_tile_rendered

project_tiles_concatenated = textwrap.indent(project_tiles_concatenated, "                ")

projects_index_template = Template(open("./templates/projects-index.html", "r").read())
projects_index_rendered = projects_index_template.render(header=header_html_string, projects=project_tiles_concatenated)

projects_index_html = open("./.public/projects/index.html", "w")
projects_index_html.write(projects_index_rendered)

#
# Create the individual skill pages
#
skill_page_template = Template(open("./templates/skill-page.html", "r").read())

for tag in project_tags:
    skill_page_html = open("./.public/projects/" + tag["id"] + ".html", "w")
    skill_page_html.write(skill_page_template.render(header=header_html_string, technology_id=tag["id"], technology_name=tag["name-nice"]))

# TODO: Fully implement blog
blog_template = Template(open("./templates/blog.html", "r").read())
blog_rendered = blog_template.render(header=header_html_string)
blog_html = open("./.public/blog.html", "w")
blog_html.write(blog_rendered)


shutil.copytree("../icons", "./.public/icons");
shutil.copytree("../pics", "./.public/pics");
shutil.copytree("../project-screenshots", "./.public/projects/project-screenshots");
shutil.copytree("../scripts", "./.public/scripts");
shutil.copytree("../styles", "./.public/styles");

shutil.copy("../favicon.ico", "./.public/favicon.ico")