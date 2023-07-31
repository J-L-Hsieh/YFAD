$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});
var feature_dict = {"GO_MF":"GO_MF", "GO_BP":"GO_BP", "GO_CC":"GO_CC", "Disease":"Disease", "Pathway":"Pathway", "Protein_Domain":"Protein Domain", "Mutant_Phenotype":"Mutant Phenotype", "Transcriptional_Regulation":"Transcriptional Regulation", "Physical_Interaction":"Physical Interaction", "Genetic_Interaction":"Genetic Interaction"}

$(document).ready(function() {
    $('.show_term_member').on("click",function(){
        var feature_name = $(this).attr('value');
        var feature = feature_name.split("*")[0];
        var name = feature_name.split("*")[1];
        $.ajax({
            url : '/yeast/ajax_p1_modal/',
            data : {'feature_name' : feature_name},
            success:function(response){
                $('#modal_table').html(response.evidence_table)
                var table_row = evidence_table.rows.length-1;
                $('#evidence_table').DataTable({
                    'bAutoWidth' : true,
                    'scrollX':true,
                    // 'scrollY' : true,
                    "scrollCollapse" : true,
                    "destroy": true,
                })
                if (feature =="Physical_Interaction"||feature =="Genetic_Interaction"){
                    $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature_dict[feature]}]: </a><a style="color:red;">${table_row} genes </a><a> have ${feature_dict[feature].toLowerCase()} with <a style="color:red;">${name}</a>`)
                }else if(feature =="Transcriptional_Regulation"){
                    $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the queried term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature_dict[feature]}]: </a><a style="color:red;">${table_row} genes </a><a> are the targets of transcriptional regulator <a style="color:red;">${name}</a>`)
                }else if(feature =="GO_MF"||feature =="GO_BP"||feature =="GO_CC"){
                    $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the queried term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature_dict[feature]}]</a>`)
                }else{
                    $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the queried term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature_dict[feature]}]</a>`)
                }

            },

            error :function(){
                alert('Something error');
            }
        })
    })
})