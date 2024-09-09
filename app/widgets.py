from ckeditor.widgets import CKEditorWidget
from django import forms

class ReadOnlyCKEditorWidget(CKEditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize CKEditor settings for read-only mode
        self.attrs['readonly'] = 'readonly'
        self.attrs['class'] = 'readonly-ckeditor'
        self.attrs['style'] = 'background-color: #f7f7f7;'


class ReadOnlyHTMLWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({
            'readonly': 'readonly',
            'style': 'background-color: #f7f7f7; border: none; width: 100%;',
            'rows': 10
        })
        super().__init__(*args, **kwargs)
