import os
import json
import textwrap
from collections import defaultdict
from jinja2 import Template

# Open the site description file
site_description_file = open("./site-desc.json", "r")
site_description = json.load(site_description_file)

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

index_html = open("../index.html", "w")
index_html.write(index_template.render(skill_grid_items=skill_grid_html_string))

#
# Create reusable project tiles to show on the various "skill" pages
#
tags_to_project_render_dict = defaultdict(list)

project_tile_template = Template(open("./templates/project-tile.html", "r").read())

projects = site_description["projects"]

project_tiles_concatenated = ""

for project in projects:
    project_tile_rendered = project_tile_template.render(project_id=project["id"], project_name=project["name-nice"], project_description=project["description"])
    for tag in project["tags"]:
        tags_to_project_render_dict[tag].append(project_tile_rendered)
    project_tiles_concatenated += project_tile_rendered

project_tiles_concatenated= textwrap.indent(project_tiles_concatenated, "                ")

projects_index_template = Template(open("./templates/projects-index.html", "r").read())
projects_index_rendered = projects_index_template.render(projects=project_tiles_concatenated)

projects_index_html = open("../projects/index.html", "w")
projects_index_html.write(projects_index_rendered)

#
# Create the individual skill pages
#
skill_page_template = Template(open("./templates/skill-page.html", "r").read())

for tag in project_tags:
    skill_page_html = open("../projects/" + tag["id"] + ".html", "w")
    skill_page_html.write(skill_page_template.render(technology_id=tag["id"], technology_name=tag["name-nice"]))