from django import forms
class ContactForm(forms.Form):
    Niveaux = [
        ('2CPI', '2 eme année'),
        ('1CS', '3 eme année'),
        ('2CS ISI', '4 eme année ISI'),
        ('2CS SIW', '4 eme année SIW'),
        ('3CS  ISI', '5 eme année ISI'),
        ('3CS  SIW', '5 eme année SIW'),
    ]
    methodes = [
        ('random', 'Random'),
        ('leader mark','leader Mark'),
        ('group mark','group Mark')
   
    ]
    promo = forms.ChoiceField(choices=Niveaux)
    method=forms.ChoiceField(choices=methodes)