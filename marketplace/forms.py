from .models import ProductItem
from django import forms
from django.core.validators import FileExtensionValidator, MaxValueValidator

    
class ProductitemForm(forms.ModelForm):
    
    class Meta:
        model =ProductItem
  
        fields= ('user_profile','product','product_description','quantity','price','location','main_image','image2','image3','product_category')
        
        widgets ={
            
            'product_description': forms.Textarea(attrs={'placeholder':'Enter Product description here...', 'row':3,})
        } 
    main_image = forms.FileField(validators=[
        FileExtensionValidator(['jpg', 'png', 'jpeg']),
        MaxValueValidator(10 * 1024 * 1024) # file size must be less than 10MB
    ])
    image2 = forms.FileField(validators=[
        FileExtensionValidator(['jpg', 'png', 'jpeg']),
        MaxValueValidator(10 * 1024 * 1024) # file size must be less than 10MB
    ])    
    image3 = forms.FileField(validators=[
        FileExtensionValidator(['jpg', 'png', 'jpeg']),
        MaxValueValidator(10 * 1024 * 1024) # file size must be less than 10MB
     ])    


    def __init__(self, *args, **kwargs):
        print('Init calles----------------------------------')
        super().__init__(*args, **kwargs)
        for field in self.fields:
            
            self.fields[ field ].widget.attrs.update({'class':'productform'})
  
  
class ProductUpdate(forms.ModelForm):
    class Meta:
        model = ProductItem

        fields = ('product','product_description','quantity','price','location','product_category','main_image','image2','image3')

        widgets ={
            
            'product_description': forms.Textarea(attrs={ 'row':5,})
        } 

    main_image = forms.FileField(validators=[
        FileExtensionValidator(['jpg', 'png', 'jpeg']),
        MaxValueValidator(10 * 1024 * 1024) # file size must be less than 10MB
    ])
    image2 = forms.FileField(validators=[
        FileExtensionValidator(['jpg', 'png', 'jpeg']),
        MaxValueValidator(10 * 1024 * 1024) # file size must be less than 10MB
    ])    
    image3 = forms.FileField(validators=[
        FileExtensionValidator(['jpg', 'png', 'jpeg']),
        MaxValueValidator(10 * 1024 * 1024) # file size must be less than 10MB
     ])    

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            
            self.fields[ field ].widget.attrs.update({'class':'productform'})
    
    def save(self, commit=True):
        productitem = self.instance
        productitem.product= self.cleaned_data['product']
        productitem.product_description= self.cleaned_data['product_description']
        productitem.quantity= self.cleaned_data['quantity']
        productitem.price= self.cleaned_data['price']
        productitem.location= self.cleaned_data['location']
        productitem.product_category= self.cleaned_data['product_category']


         
        if self.cleaned_data ['main_image']:
            productitem.field= self.cleaned_data['main_image']
        if self.cleaned_data ['image2']:
            productitem.field= self.cleaned_data['image2']
        if self.cleaned_data ['image3']:
            productitem.field= self.cleaned_data['image3']

        if commit:
            productitem.save()
        return productitem

  
  