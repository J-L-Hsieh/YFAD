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
            let trs = document.querySelectorAll('#both_name_table tr');

            for (let tr of trs) {
                let td = document.createElement('td');
                tr.appendChild(td);
            }
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
                    },
                    {   'targets':3,
                        render:function(data,type,row,meta){
                            return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${first_feature_array[0]}%${second_feature_array[0]}%${row[0]}" name ="${row[1]}%${row[2]}"> Evidence </a>`
                        },
                    },
                ]
            })
            $('#both_name_table').on("click",'.modal_features',function(){
                var feature = $(this).attr('value');
                var t_or_f = $(this).attr('name').split('%');
                var feature1_exist = t_or_f[0]
                var feature2_exist = t_or_f[1]

                $.ajax({
                    url : '/yeast/ajax_evidence/',
                    data : {'feature' : feature},
                    success:function(response){
                        if (feature1_exist ==='true'){
                            $('#feature1').html(response.feature1_table)
                            $('#feature1_table').DataTable()
                        }
                        else{
                            $('#feature1').html('<div></div>')
                        }

                        if (feature2_exist ==='true'){
                            $('#feature2').html(response.feature2_table)
                            $('#feature2_table').DataTable()
                        }
                        else{
                            $('#feature2').html('<div></div>')
                        }
                    },
                    error :function(){
                        alert('Something error');
                    }
                })
            })
        },
        error:function(){
            alert('Something error');
        }
    })
})