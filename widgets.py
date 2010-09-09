"""
Dojo Widget set for Django

Widgets imported so far:
    - dijit.form.DateTextBox
    - dijit.form.ValidationTextBox
    
@author
"""

from django.forms.widgets import DateInput, TextInput, Select
import logging

class DojoWidgetBase(object):
    # Form Required Fields
    dojo_name = None
    dojo_value = None
    
    dojo_readonly = """
    dijit.byId('%(name)s').set('readOnly',true);
    """
    
    # Additional Fields
    regex = None
    required = False
    prompt_message = None
    invalid_message = None
    
    def get_dojo_callback(self):
        """returns the callback javascript"""
        extra = ""
        if self.attrs.get('readonly'):
            extra = self.dojo_readonly % {'name': self.dojo_name}
        return self.dojo_callback % {'name': self.dojo_name, 'extra': extra}
        
    def render(self, name, value, attrs=None):
           self.dojo_value = value
           return "<input type='hidden' id='%(name)s' name='%(name)s' value='%(value)s'/>" % {'name':self.dojo_name, 'value':value if value else ''}
    
class DojoSelectWidget(DojoWidgetBase, Select):

    dojo_type = ["dojo.data.ItemFileReadStore", "dijit.form.Select"]
    dojo_callback = """
var %(name)s_store = new dojo.data.ItemFileReadStore({data: {identifier: 'id',label: 'name',items: [%(items)s]}});
new dijit.form.Select({name: "%(name)s",id: "%(name)s",store: %(name)s_store,value: dojo.byId('%(name)s').value}, dojo.byId('%(name)s')).startup();
%(extra)s
    """
    
    def get_dojo_callback(self):
        extra = ""
        items = []
        for x in self.choices:
            items.append("{id: '%d', name: '%s'}" % (x[0], x[1]))
        if self.attrs.get('readonly'):
            extra = self.dojo_readonly % {'name': self.dojo_name}
        return self.dojo_callback % {'name': self.dojo_name, 'extra': extra, 'items': ",".join(items)}
        
    
class DojoDateWidget(DojoWidgetBase, DateInput):

    dojo_type = "dijit.form.DateTextBox"
    dojo_readonly = """dijit.byId('%(name)s').set('readOnly',true);"""
    dojo_callback = """
new dijit.form.DateTextBox({name: "%(name)s",
    constraints: {datePattern:'yyyy-MM-dd'},
    value: new Date(dojo.byId('%(name)s').value),
    onKeyUp: function(v){if(this.isValid()){this._picker.attr('value', this.attr('value'));}}
    }, dojo.byId('%(name)s'));
%(extra)s
"""

        
class DojoValidatingTextWidget(DojoWidgetBase, TextInput):

    dojo_type =  "dijit.form.ValidationTextBox"
    dojo_callback = """
new dijit.form.ValidationTextBox(
{name: '%(name)s',required: %(required)s,invalidMessage: "%(invalid)s",regExp: "%(regex)s"}, 
dojo.byId('%(name)s'));"""
    
    def __init__(self, regex, required = False, prompt_message = None, invalid_message = None, attrs = None):
        """DojoValidationTextWidget
            args:
            required = boolean
            prompt_message = tooltip text
            invalid_message = tooltip text when you enter invalid info
            regex = regular expression string to validate against
        """
        super(DojoValidatingTextWidget, self).__init__(attrs)
        self.regex = regex
        self.required = required
        self.prompt_message = prompt_message
        self.invalid_message = invalid_message
    
    def get_dojo_callback(self):
        """returns the callback javascript lines"""
        return self.dojo_callback % {'required' : "true" if self.required else "false",
                'invalid' : self.invalid_message,
                'regex' : self.regex,
                'name' : self.dojo_name}       