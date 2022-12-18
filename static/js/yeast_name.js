$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});
$(document).ready(function() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const first_feature = urlParams.get('id')
    const second_feature = urlParams.get('name')
    var first_feature_array = first_feature.split('$')
    var second_feature_array = second_feature.split('$')

    $('#first').html(`<p>Queried : ${first_feature_array[0]}  Term : ${first_feature_array[1]}`)
    $('#second').html(`<p>Feature : ${second_feature_array[0]}  Term : ${second_feature_array[1]}`)

    $.ajax({
        url : '/yeast/ajax_name/',
        data : { 'first_feature' : first_feature,'second_feature' : second_feature },
        success:function(response){
            $('#Answer1').html(response.df_merge)
            $('#both_name_table').DataTable({
                'columnDefs':[
                    {   'targets':1,
                        render:function(row){
                            if (row ==='true'){
                                return '<div>&#9989</div>'
                            }else{
                                return '<div>&#10060</div>'
                            }
                        }
                    },
                    {   "target":2,
                        render: function(row){
                            if (row ==='true'){
                                return '<div>&#9989</div>'
                            }else{
                                return '<div>&#10060</div>'
                            }
                        }
                    }
                ]
            })
        },
        error:function(){
            alert('Something error');
        }
    })
})