from django import forms

from manage_article_drive.models import Article, Tag


class MultipleSelectCheckboxForm(forms.Form):
    select = forms.ModelMultipleChoiceField(queryset=Article.objects.all(),
                                             widget=forms.CheckboxSelectMultiple())

class SearchTextForm(forms.Form):
    search_phrase = forms.CharField(label='Search phrase', max_length=100)

# class SearchTagForm(forms.Form):
#     search_tag = forms.CharField(label='Search tag', max_length=100)

# class SearchTagForm(forms.Form):
#     tag_select = forms.ModelMultipleChoiceField(queryset=None)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['tag_select'].queryset = Tag.objects.distinct()
#     # tag = forms.ModelChoiceField(queryset=Tag.objects.all().order_by('tag_text'))


class SearchDatesForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
