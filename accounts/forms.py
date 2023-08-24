from django import forms

from accounts.models import Account

class RegisterationForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
    }))
    
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    }))
    
    class Meta:
        model = Account
        fields=['first_name','last_name','phone_number','email','password']
    
    # apply css class on all form fields
    def __init__(self,*args, **kwargs):
        super(RegisterationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder']='Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    
    # validate input form data
    # note: there are two types of errors field error and none field error in below function we use 
    #       none field error as we raise the excetion manualy
    # ex: [ form.errors ] -> that display none field errors and [ form.none_field_errors]
    
    def clean(self):
        clean_data= super(RegisterationForm,self).clean()
        password=clean_data.get('password')
        confirm_password=clean_data.get('confirm_password')
        if password!= confirm_password:
            raise forms.ValidationError("Password does not match.")