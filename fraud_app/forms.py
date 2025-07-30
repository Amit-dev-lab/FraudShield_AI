from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

CITIES = [
    ('Columbia', 'Columbia'), ('Altonah', 'Altonah'), ('Bellmore', 'Bellmore'),
    ('Titusville', 'Titusville'), ('Falmouth', 'Falmouth'), ('Breesport', 'Breesport'),
    ('Carlotta', 'Carlotta'), ('Spencer', 'Spencer'), ('Morrisdale', 'Morrisdale'),
    ('Prairie Hill', 'Prairie Hill'), ('Westport', 'Westport'), ('Fort Washakie', 'Fort Washakie'),
    ('Loxahatchee', 'Loxahatchee'), ('Rock Tavern', 'Rock Tavern'), ('Jones', 'Jones'),
    ('Deltona', 'Deltona'), ('Key West', 'Key West'), ('Grandview', 'Grandview'),
    ('Saint Amant', 'Saint Amant'), ('Clarks Mills', 'Clarks Mills'), ('Alpharetta', 'Alpharetta'),
    ('Colorado Springs', 'Colorado Springs'), ('Greenville', 'Greenville'), ('Tomahawk', 'Tomahawk'),
    ('Goodrich', 'Goodrich'), ('Daly City', 'Daly City'), ('South Londonderry', 'South Londonderry'),
    ('Lepanto', 'Lepanto'), ('New Waverly', 'New Waverly'), ('New York City', 'New York City'),
    ('Pewee Valley', 'Pewee Valley'), ('Plainfield', 'Plainfield'), ('Belmond', 'Belmond'),
    ('Bagley', 'Bagley'), ('Manchester', 'Manchester'), ('Sontag', 'Sontag'),
    ('Hawthorne', 'Hawthorne'), ('Gadsden', 'Gadsden'), ('Birmingham', 'Birmingham'),
    ('Ollie', 'Ollie'), ('Baton Rouge', 'Baton Rouge'), ('San Antonio', 'San Antonio'),
    ('Southfield', 'Southfield'), ('Mc Cracken', 'Mc Cracken'), ('Purmela', 'Purmela'),
    ('Lomax', 'Lomax'), ('Tuscarora', 'Tuscarora'), ('Sunflower', 'Sunflower'),
    ('Ogdensburg', 'Ogdensburg'), ('Redford', 'Redford'), ('Brooklin', 'Brooklin'),
    ('Fields Landing', 'Fields Landing'), ('Rocky Mount', 'Rocky Mount')
]

CATEGORIES = [
    ('personal_care', 'Personal Care'),
    ('health_fitness', 'Health & Fitness'),
    ('misc_pos', 'Miscellaneous POS'),
    ('travel', 'Travel'),
    ('kids_pets', 'Kids & Pets'),
    ('shopping_pos', 'Shopping POS'),
    ('food_dining', 'Food & Dining'),
    ('home', 'Home'),
    ('entertainment', 'Entertainment'),
    ('shopping_net', 'Shopping Online'),
    ('misc_net', 'Miscellaneous Online'),
    ('grocery_pos', 'Grocery POS'),
    ('gas_transport', 'Gas & Transport'),
    ('grocery_net', 'Grocery Online'),
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class FraudCheckForm(forms.Form):
    trans_date_trans_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Transaction Date & Time'
    )
    category = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Category'
    )
    amount_inr = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label='Amount (INR)'
    )
    sender_city = forms.ChoiceField(
        choices=CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Sender City'
    )
    receiver_city = forms.ChoiceField(
        choices=CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Receiver City'
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date of Birth'
    )
    has_previous_transaction = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Has Previous Transaction'
    )
    previous_transaction_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Previous Transaction Date (if applicable)'
    )
