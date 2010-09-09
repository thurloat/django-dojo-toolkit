# Django Dojo Toolkit #

This is our implementation of Various Dojo Dijit Widgets and Dojo Forms.

# Sample Usage #

in forms.py:

        from django import forms
        from dojotoolkit.forms import DojoForm
        from dojotoolkit.widgets import DojoDateWidget, DojoValidatingTextWidget, DojoSelectWidget
        
        class FooForm(DojoForm):
            name = forms.CharField(widget = DojoValidatingTextWidget("[a-zA-Z ]+", required=True, invalid_message="don't use numbers"))
        
            def save(self):
                #save your model using self.cleaned_data
                return instance
                
in your template:

        {% extends "base.html" %}
        {% block preload_js %}
            {{ form.get_dojo_js }}
        {% endblock %}
        {% block content %}
            <form method="POST" id="new-thing" dojoType="dijit.form.Form" onsubmit="return this.validate();">
                <table>
                    {{ form.as_table }}
                </table>
                {{ form.get_submit_button }}
            </form>
        {% endblock %}
        
# Additional Notes #

 - Call Adam or Sam!