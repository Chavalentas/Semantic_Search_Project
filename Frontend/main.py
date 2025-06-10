import gradio as gr
import json
from models.helper import Helper
from models.paper import Paper
from config import Config
from services import title_search_service, abstract_search_service

# # Load services and the configuration file
config_file = Config()
title_service = title_search_service.TitleSearchService()
abstract_service = abstract_search_service.AbstractSearchService()
app_settings = dict()

with open(config_file.app_settings_path) as settings_path:
    app_settings = json.load(settings_path)

# Helper functions
def generate_html_div(paper: Paper) -> str:
    """Creates a HTML div container for the given paper.

    Args:
        paper (Paper): The paper.

    Returns:
        str:  String containing the HTML structure of the container.
    """
    Helper.ensure_instance(paper, Paper, "paper must be an instance of Paper!")
    title = Helper.replace_pattern(paper.get_title(), "\n", lambda x: '<br/>',
                                                             True)
    date_time = Helper.replace_pattern(paper.get_datetime(), "\n", lambda x: '<br/>',
                                                             True)
    authors = ",".join([a.get_full_name() for a in paper.get_authors()])
    abstract = Helper.replace_pattern(paper.get_abstract(), "\n", lambda x: '<br/>',
                                    True)
    result = f"""
    <div style="border-radius: 5px;border-width: medium;">
        <h4>Title </h4>
        <div style="overflow-y: auto; height:50px; border-radius: 5px;border-width: medium; margin-left: 5px; margin-right: 5px; margin-top: 5px; margin-bottom: 5px;">
            {title}
        </div>
        <h4>Date of publication</h4>
        <div style="overflow-y: auto; height:50px; border-radius: 5px;border-width: medium;
        margin-left: 5px; margin-right: 5px; margin-top: 5px; margin-bottom: 5px;">
            {date_time}
        </div
        <h4>Authors</h4>
        <div style="overflow-y: auto; height:50px; border-radius: 5px;border-width: medium;
        margin-left: 5px; margin-right: 5px; margin-top: 5px; margin-bottom: 5px;">
            {authors}
        </div>
        <h4>Abstract</h4>
        <div style="overflow-y: auto; height:200px; border-radius: 5px;border-width: medium;
        margin-left: 5px; margin-right: 5px; margin-top: 5px; margin-bottom: 5px;">
            {abstract}
        </div>
    </div>"""
    return result

#----------------------------------------------
#---------------------UI-----------------------
#----------------------------------------------
title_block = gr.Blocks()
abstract_block = gr.Blocks()
regex_parentheses = [("\\(", "\\("), ("\\)", "\\)"), ("\\[", "\\["),
                           ("\\]", "\\]"), ("\\{", "\\{"), ("\\}", "\\}")]

# The title semantic/lexical search
with title_block as tab_subblock_1:
    results = gr.State([])
    query_input = gr.Textbox(placeholder="Enter your request", label="Title query", max_lines=1)
    slider_val = gr.Slider(app_settings["perTitleMin"], app_settings["perTitleMax"], step=1, label="Amount",
                           info=f"Choose between {app_settings['perTitleMin']} and {app_settings['perTitleMax']}", interactive=True,
                           show_label=True, render=True)
    choice = gr.Radio(choices=["lexical", "semantic"], label="Query type", value="lexical")
    submit_button = gr.Button(variant='primary', value="Submit", size='sm', elem_classes="submit-button")
    gr.Markdown("## Results: ")

    @gr.render(inputs=[query_input, slider_val, choice], triggers=[submit_button.click])
    def handle_button_click(query: str, slider_val: int, choice: str):    
        if len(query) == 0:
            gr.Warning("The query cannot be empty!", 5)
            return
        
        if not(slider_val >= app_settings["perTitleMin"] and slider_val <= app_settings["perTitleMax"]):
            gr.Warning(f"The slider value was out of range! (min: {app_settings['perTitleMin']}, max: {app_settings['perTitleMax']})", 5)
            return
        
        if choice is None:
            gr.Warning("Pick either semantic or lexical search!", 5)
            return
        
        gr.Info("Fetching data... Please wait...", duration=0)
        
        try:
             if choice == "semantic":   
                response = title_service.search_by_title(query, slider_val)    

                if len(response) == 0:
                    gr.Markdown("### No results found!")
                    return

                for el in response:
                    with gr.Blocks():
                        to_render =Paper(el.get_id(), el.get_title(), el.get_abstract(), el.get_datetime(), el.get_authors())
                        gr.HTML(generate_html_div(to_render))
            
             if choice == "lexical":
                query = Helper.replace_patterns(query, regex_parentheses, True)
                response = title_service.search_by_title_lexical(query, slider_val)   

                if len(response) == 0:
                    gr.Markdown("### No results found!")
                    return 

                for el in response:
                    with gr.Blocks():
                        title_replaced = Helper.replace_pattern(el.get_title(), query, lambda x: f'<span style="color:red">{x}</span>',
                                                             False)
                        to_render = Paper(el.get_id(), title_replaced, el.get_abstract(), el.get_datetime(), el.get_authors())
                        gr.HTML(generate_html_div(to_render))

             gr.Info("Data were successfully fetched!", duration=0)
        except Exception as e:
            gr.Warning("Some error occurred! Try again later!" + str(e), duration=5)

# The abstract semantic/lexical search
with abstract_block as tab_subblock_2:
    results = gr.State([])
    query_input = gr.Textbox(placeholder="Enter your request", label="Abstract query", max_lines=1)
    slider_val = gr.Slider(app_settings["perAbstractMin"], app_settings["perAbstractMax"], step=1, label="Amount",
                           info=f"Choose between {app_settings['perAbstractMin']} and {app_settings['perAbstractMax']}", interactive=True,
                           show_label=True, render=True)
    choice = gr.Radio(choices=["lexical", "semantic"], label="Query type", value="lexical")
    submit_button = gr.Button(variant='primary', value="Submit", size='sm', elem_classes="submit-button")
    gr.Markdown("## Results: ")

    @gr.render(inputs=[query_input, slider_val, choice], triggers=[submit_button.click])
    def handle_button_click(query: str, slider_val: int,  choice: str):
        if len(query) == 0:
            gr.Warning("The query cannot be empty!", 5)
            return
        
        if not(slider_val >= app_settings["perAbstractMin"] and slider_val <= app_settings["perAbstractMax"]):
            gr.Warning(f"The slider value was out of range! (min: {app_settings['perAbstractMin']}, max: {app_settings['perAbstractMax']})", 5)
            return
        
        if choice is None:
            gr.Warning("Pick either semantic or lexical search!", 5)
            return
        
        gr.Info("Fetching data... Please wait...", duration=0)
        
        try:
            if choice == "semantic":   
                response = abstract_service.search_by_abstract(query, slider_val) 

                if len(response) == 0:
                    gr.Markdown("### No results found!")
                    return

                for el in response:
                    with gr.Blocks(theme=gr.themes.Monochrome()):
                        paper = el.get_paper()
                        chunks = el.get_chunks()
                        patterns = [el.get_text() for el in chunks]
                        patterns_replaced = [Helper.replace_patterns(el, regex_parentheses, True) for el in patterns]
                        pattern_to_funcs = [(el, f'<span style="color:red">{patterns[i]}</span>') for i, el in enumerate(patterns_replaced)]
                        abstract_replaced = Helper.replace_patterns(paper.get_abstract(), pattern_to_funcs,
                                                                    True)
                        to_render = Paper(paper.get_id(), paper.get_title(), abstract_replaced, paper.get_datetime(), paper.get_authors())
                        gr.HTML(generate_html_div(to_render))

            if choice == "lexical":
                response = abstract_service.search_by_abstract_lexical(query, slider_val) 

                if len(response) == 0:
                    gr.Markdown("### No results found!")
                    return

                for el in response:
                    with gr.Blocks():
                        query = Helper.replace_patterns(query, regex_parentheses, True)
                        abstract_replaced = Helper.replace_pattern(el.get_abstract(), query, lambda x: f'<span style="color:red">{x}</span>',
                                                             False)
                        to_render =Paper(el.get_id(), el.get_title(), abstract_replaced, el.get_datetime(), el.get_authors())
                        gr.HTML(generate_html_div(to_render))

            gr.Info("Data were successfully fetched!", duration=0)
        except Exception as e:
            gr.Warning("Some error occurred! Try again later!" + str(e), duration=5)


# The main UI block containing the tabs with the title and abstract semantic search (title AND abstract)
main_block = gr.Blocks(theme=gr.themes.Default(neutral_hue="blue", primary_hue="neutral"))
with main_block as mb:
    tabbed_interface = gr.TabbedInterface([tab_subblock_1, tab_subblock_2], ["Title", "Abstract"])

if __name__ == "__main__":
    mb.launch()