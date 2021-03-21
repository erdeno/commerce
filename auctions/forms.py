from django import forms

from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "category",
            "description",
            "image_url",
            "starting_price",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": "5",}
            ),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
            "starting_price": forms.NumberInput(attrs={"class": "form-control"}),
        }
