{% extends "mail_templated/base.tpl" %}

{% block subject %}
Todo website reset password
{% endblock %}

{% block html %}
http://127.0.0.1:8000/api/v1/reset-password/uid/{{user_id}}/{{token}}
{% endblock %}