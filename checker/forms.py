from django import forms

from .constants import CODE_FORM_FIELD_PLACEHOLDER


class CheckNewCodeForm(forms.Form):
    def __init__(self, language_choices, *args, **kwargs):
        super(CheckNewCodeForm, self).__init__(*args, **kwargs)
        self.fields["language"].choices = language_choices

    code = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": CODE_FORM_FIELD_PLACEHOLDER,
                "class": "form-control text-area-resize-none",
                "rows": 12,
            },
        ),
        required=True,
    )
    language = forms.ChoiceField(
        widget=forms.Select(
            attrs={"class": "form-select w-50"},
            choices=(),
        ),
        required=False,
    )
    run_ai = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    run_static = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        run_ai = cleaned_data.get("run_ai")
        run_static = cleaned_data.get("run_static")

        if not run_ai and not run_static:
            raise forms.ValidationError("None of the available checks is choosen!")
