from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))

        # Применяем класс 'form-check-input' к булевым полям
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == "CheckboxInput":
                field.widget.attrs.update({"class": "form-check-input"})
