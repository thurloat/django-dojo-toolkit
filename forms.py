from django import forms
from django.utils.safestring import mark_safe
from django.template import TemplateSyntaxError
import logging
class DojoForm(forms.Form):
    dojo = """
    <script src="http://ajax.googleapis.com/ajax/libs/dojo/1.5/dojo/dojo.xd.js" djConfig="parseOnLoad:true"></script>
    <script>
        function loader() {
            dojo.require('dijit.form.Form');
            dojo.require('dijit.form.Button');
            %s
            dojo.addOnLoad(callback);
        }
        function callback(){
            %s
        }

        dojo.addOnLoad(loader);
    </script>
    """

    def __init__(self, *args):
        super(DojoForm, self).__init__(*args)
        
    def get_dojo_js(self):
        """
            Scans through all included fields, then attempts to access their dojo type
            and dojo callback function for bootstrapping it up.
        """
        dojo_requires = []
        dojo_callbacks = []
        for name, value in self.fields.items():
            # Iterate through all the fields in the form, and see if they're a dojo widget
            if hasattr(value.widget, 'dojo_name'):
                value.widget.dojo_name = name
                # Includes the dojo require for a specified widget
                req_list = value.widget.dojo_type
                
                if not isinstance(req_list, list):
                    req_list = [value.widget.dojo_type,]

                for req in req_list:
                    dojo_requires.append("dojo.require('%s');" % req)

                dojo_callbacks.append(value.widget.get_dojo_callback())
        
        return mark_safe(u'\n' + self.dojo % 
                    ('\n'.join(set(dojo_requires)),
                    '\n'.join(dojo_callbacks)))
    
    def get_submit_button(self):
        """renders a dojo submit button with validating codez"""
        button = """
<button dojoType="dijit.form.Button" type="submit" name="submit" value="Submit">Submit</button>
        """
        return mark_safe(button)
        
        