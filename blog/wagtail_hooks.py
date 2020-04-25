import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler


@hooks.register('register_rich_text_features')
def register_help_text_feature(features):
    """
    Registering the `help-text` feature, which uses the `help-text` Draft.js block type,
    and is stored as HTML with a `<div class="help-text">` tag.
    """
    feature_name = 'blockquote-text'
    type_ = 'blockquote-text'

    control = {
        'type': type_,
        'label': '"',
        'description': 'blockquote',
        # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
        'element': 'div',
        'style': {
            'display':'block',
            'background':'yellow',
        },
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['help-text.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'div[class=blockquote-holder with-bg-2]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'blockquote-holder with-bg-2'}}}},
    })

    features.default_features.append('blockquote-text')

