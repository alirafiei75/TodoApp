{% extends "mail_templated/base.tpl" %}

{% block subject %}
Todo website account verification
{% endblock %}

{% block html %}
http://127.0.0.1:8000/api/v1/verification/confirm/{{token}}
{% endblock %}