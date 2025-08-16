document.addEventListener("DOMContentLoaded", function() {
    $('.select2-field').select2({
        theme: 'bootstrap',
        placeholder: 'Escolha uma opção...',
        allowClear: true,
        width: '100%'
    });
});