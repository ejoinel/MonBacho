/**
 * Created by Pau on 10/03/2016.
 */

$(document).ready( function() {
       // .... your jQuery goodness ....
    tooltip_help();
    place_horder_input_file();
    panel_collapse();
 })



function tooltip_help(){
    $('select.selectpicker').attr('data-live-search', 'true');
    $('[data-toggle="tooltip"]').tooltip();
}



function panel_collapse(){
    $('.panel-heading span.clickable').on("click", function (e) {
    if ($(this).hasClass('panel-collapsed')) {
        // expand the panel
        $(this).parents('.panel').find('.panel-body').slideDown();
        $(this).removeClass('panel-collapsed');
        $(this).find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
    }
    else {
        // collapse the panel
        $(this).parents('.panel').find('.panel-body').slideUp();
        $(this).addClass('panel-collapsed');
        $(this).find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    }
})
}



function place_horder_input_file(){
    $(":file").filestyle({buttonName: "btn-primary", buttonText: "Choisir", size: "sm", placeholder: "Entrez un image"});
        $('.form-inline').formset({
            addText: 'Ajouter',
            deleteText: 'Supprimer'
        });

	return this;
}

$(function(){

	$('#slide-submenu').on('click',function() {
        $(this).closest('.list-group').fadeOut('slide',function(){
        	$('.mini-submenu').fadeIn();
        });

      });

	$('.mini-submenu').on('click',function(){
        $(this).next('.list-group').toggle('slide');
        $('.mini-submenu').hide();
	})
})
