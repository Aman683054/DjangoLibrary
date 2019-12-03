from django import forms
from myapp.models import Order, Review, Member, User


class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    name = forms.CharField(label="Enter Your Name:", max_length=100, required=False)
    category = forms.ChoiceField(label="Select a Category:", widget=forms.RadioSelect, choices=CATEGORY_CHOICES,
                                 required=False)
    max_price = forms.IntegerField(label="Maximum Price:", min_value=0)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'status', 'address', 'city', 'province', 'auto_renew', 'avatar']
        widgets = {'status': forms.RadioSelect(), 'auto_renew': forms.CheckboxInput()}
        labels = {'avatar': u'Profile Picture'}


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        # labels = {'member': u'Member name', }



class ReviewForm(forms.ModelForm):
    class Meta:
        # Rating_choices = [
        #     (1, "Not so good"),
        #     (2, "Below Average"),
        #     (3, "Average"),
        #     (4, "Good"),
        #     (5, "Excellent")
        # ]
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {'reviewer': forms.EmailInput(),
                   'book': forms.RadioSelect(),
                   'rating': forms.NumberInput(),
                   'comments': forms.Textarea()
                   }
        labels = {'reviewer': u"Please enter a valid Email Id", 'rating': u"Rating"}



