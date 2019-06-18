from django.forms import ModelForm
from .models import Profile

class ProfileForm(ModelForm):
    # picture = forms.CharField(label='Picture', max_length=100)
    # employer = forms.CharField(label='Employer', max_length=50)
    # isDriver = forms.BooleanField(default=False)
    class Meta:
        model = Profile
        fields = ['picture', 'employer']