import os
import json
import textwrap
import shutil
from collections import defaultdict
from jinja2 import Template
from highlight_code_blocks import highlight_code_in_html

def load_template(path):
    with open(path, "r") as file:
        return Template(file.read())


def write_to_file(path, content):
    with open(path, "w") as file:
        file.write(content)

# Set the working directory to be this folder (In case the user tries to execute it from a different
# directory; which would break the relative paths)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Clear the public directory if it exists, then create it
if os.path.exists("./.public"):
    shutil.rmtree("./.public")
os.mkdir("./.public")
os.mkdir("./.public/projects")


# Load the site description file
site_description_file = open("./site-desc.json", "r")
site_description = json.load(site_description_file)

# Load the HTML for the page header, which will be reused on several pages
header_html_string = open("./templates/header.html").read()
header_html_string = textwrap.indent(header_html_string, "        ")


# In this next section, we create a link tile for each possible "skill" that a project can be tagged
# with; they  all link to a page showcasing projects that use that skill.

# Get all of the possible tags that can be applied to a project
project_tags = site_description["project-tags"]

# Open the template for the link tile (the skill-grid-item.html)
skill_grid_template = load_template("./templates/skill-grid-item.html")

# All of the rendered tiles are appended to a single string, so they can easily be added to the
# homepage.
skill_grid_html_string = ""

# Open the template for the homepage
index_template = load_template("./templates/index.html")

# Create the tiles and append them to the string
for tag in project_tags.values():
    tag_id = tag["id"]
    tag_name = tag["name-nice"]
    result = skill_grid_template.render(project_tag=tag_id, tag_name_nice=tag_name)
    skill_grid_html_string = skill_grid_html_string + result + "\n"

skill_grid_html_string = textwrap.indent(skill_grid_html_string, "                    ")

# Render and write the finished homepage to file
index_rendered = index_template.render(
    skill_grid_items=skill_grid_html_string, header=header_html_string
)
index_html_path = "./.public/index.html"
write_to_file(index_html_path, index_rendered)

# Now, we create tiles for all projects. These tiles are used on the "Projects" page, as well as the
# pages dedicated to individual skills.

# The idea here is that each project tile is appended to a single string for display on the
# "Projects" page, but we also check what tags that project has, and create a dictionary with tags
# as the keys and string lists of rendered HTML project

# Create the skills-to-projects dictionart (using defaultdict for convenience sake)
tags_to_project_render_dict = defaultdict(list)

# Get the template for a project tile
project_tile_template = load_template("./templates/project-tile.html")

# Retrieve all projects
projects = site_description["projects"]

# This is the string that will be inserted into the "Projects" page
project_tiles_concatenated = ""

# Render the project tiles, filling the dictionary and the concatenated string.
for project in projects:
    project_tile_rendered = project_tile_template.render(
        project_id=project["id"], project_name=project["name-nice"]
    )
    for tag in project["tags"]:
        tags_to_project_render_dict[tag].append(project_tile_rendered)
    project_tiles_concatenated += project_tile_rendered
project_tiles_concatenated = textwrap.indent(project_tiles_concatenated, "                ")

# Create the Projects page
projects_index_template = load_template("./templates/projects-index.html")
projects_index_rendered = projects_index_template.render(
    header=header_html_string, projects=project_tiles_concatenated
)
projects_index_html_path = "./.public/projects/index.html"
write_to_file(projects_index_html_path, projects_index_rendered)

# Now, we create the pages to show off projects that use a particular skill
skill_page_template = load_template("./templates/skill-page.html")
for tag in project_tags.values():
    tiles = "\n".join(tags_to_project_render_dict[tag["id"]])
    tiles = textwrap.indent(tiles, "                ")
    skill_page_rendered = skill_page_template.render(
        header=header_html_string,
        technology_id=tag["id"],
        technology_name=tag["name-nice"],
        project_tiles=tiles,
    )
    skill_page_html_path = "./.public/projects/" + tag["id"] + ".html"
    write_to_file(skill_page_html_path, skill_page_rendered)

# Now we want to create the project-specific pages.
# The templates for these ones are very presentation-agnostic; each one can have custom HTML.
# The contents for the project pages is at templates/project-pages/
project_page_template = load_template("./templates/project-page.html")
tag_chip_template = load_template("./templates/tag-chip.html")

for project in projects:
    project_page_content = open(
        "./templates/project-pages/" + project["id"] + ".html", "r"
    ).read()
    project_page_content = textwrap.indent(project_page_content, "            ")
    tag_chips_html_string = ""

    for tag in project["tags"]:
        tag_chip_rendered = tag_chip_template.render(
            tag=tag, skill_name=project_tags[tag]["name-nice"]
        )
        tag_chips_html_string += tag_chip_rendered + "\n"
    tag_chips_html_string = textwrap.indent(tag_chips_html_string, "                    ")
    
    project_page_rendered = project_page_template.render(
        header=header_html_string,
        project_name=project["name-nice"],
        project_page_contents=project_page_content,
        link=project["link"],
        tag_chips=tag_chips_html_string,
    )
    project_page_rendered = highlight_code_in_html(project_page_rendered)
    project_page_html_path = "./.public/projects/" + project["id"] + ".html"
    write_to_file(project_page_html_path, project_page_rendered)

# TODO: Fully implement blog
blog_template = load_template("./templates/blog.html")
blog_rendered = blog_template.render(header=header_html_string)
blog_html_path = "./.public/blog.html"
write_to_file(blog_html_path, blog_rendered)

# I could have done this part in the workflow file, but it's probably best to keep all of the file
# operations in one place.
shutil.copytree("../icons", "./.public/icons")
shutil.copytree("../pics", "./.public/pics")
shutil.copytree("../project-screenshots", "./.public/projects/project-screenshots")
shutil.copytree("../scripts", "./.public/scripts")
shutil.copytree("../styles", "./.public/styles")
shutil.copytree("../content", "./.public/content")

shutil.copy("../favicon.ico", "./.public/favicon.ico")
