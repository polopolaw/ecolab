from django import forms



class ReviewForm(forms.Form):
    author_name = forms.CharField(max_length=140)
    author_email = forms.EmailField()
    author_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    author_avatar = forms.CharField(widget=forms.HiddenInput(), required=False)
    review_content = forms.CharField(widget=forms.Textarea, max_length=800)
    vote = forms.IntegerField(widget=forms.NumberInput(attrs={'max' : 5, 'min': 1}))
    pros = forms.CharField(widget=forms.Textarea, max_length=800, required=False)
    cons = forms.CharField(widget=forms.Textarea(), required=False)
    wasrecomeded = forms.BooleanField(widget=forms.CheckboxInput(), required=False)