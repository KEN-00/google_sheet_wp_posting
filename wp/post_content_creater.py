from jinja2 import Environment, BaseLoader

def create_post_content(postData, jinja2PostTemplate):
    return jinja2PostTemplate.render(postData)

def create_jinja2_post_template(jinja2PostTemplateString):
    jinja2PostTemplate = Environment(loader=BaseLoader()).from_string(jinja2PostTemplateString)
    return jinja2PostTemplate