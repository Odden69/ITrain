// code for adding additional forms to the formset was copied from
// https://simpleit.rocks/python/django/dynamic-add-form-with-add-button-in-django-modelformset-template/

$('#add_more').click(function() {
	var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});