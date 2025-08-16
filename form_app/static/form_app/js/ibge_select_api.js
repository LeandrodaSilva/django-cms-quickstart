$.get(window.IBGE_API_URL)
    .done(function(estados) {
        const selectEstado = $(`#estado-${window.INSTANCE_PK}`);
        selectEstado.empty().append('<option value="">Selecione o estado</option>');
        estados.forEach(estado => {
            selectEstado.append(`<option value="${estado.sigla}">${estado.nome}</option>`);
        });
        selectEstado.prop('disabled', false);
    })
    .fail(function() {
        $(`#estado-${window.INSTANCE_PK}`).html('<option value="">Erro ao carregar estados</option>');
    });

$(document).on('change', `#estado-${window.INSTANCE_PK}`, function() {
    const uf = $(this).val();
    if (!uf) return;
    const selectCidade = $(`#cidade-${window.INSTANCE_PK}`);
    selectCidade.prop('disabled', true).html('<option value="">Carregando...</option>');
    
    $.get(`${window.IBGE_API_URL}?uf=${uf}`)
        .done(function(municipios) {
            selectCidade.empty().append('<option value="">Selecione a cidade</option>');
            municipios.forEach(municipio => {
                selectCidade.append(`<option value="${municipio.nome}">${municipio.nome}</option>`);
            });
            selectCidade.prop('disabled', false);
        })
        .fail(function() {
            selectCidade.html('<option value="">Erro ao carregar cidades</option>');
        });
});
