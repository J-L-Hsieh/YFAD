$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
})



$(document).ready(function(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const row_name = urlParams.get('id')
    const table_name = urlParams.get('name')
    $('#queried').html(`<p>Queried ${table_name} Term : ${row_name}`)
    $('#associated_title').html(`<p>Associated Term with the Queried ${table_name} Term `)

    console.log(table_name,row_name)
    // create a network

    $.ajax({
        url : '/yeast/ajax_associated/',
        data : {'table_name':table_name, 'row_name':row_name},
        success:function(response){
            console.log('-----')

            $('#Answer1').html(response.associated_table);
            $('#associated_table').DataTable();
            var column_order = response.all_tables.column_order
            /* --------------------------network graph----------------------------*/
            // for (i=0 ;i<all_title_name.length; i++){
            //     $('#nodeFilterSelect').append(`<option value=${all_title_name[i]}>${all_title_name[i]}</option>`)
            // }
            var data = response.network_data
            var options = {
                // nodes:{
                //     type:'rectangle'
                // },
                edges:{
                    arrows:{
                        to:{enabled:true, type: 'arrow'}
                    },
                }
            };
            var container = document.getElementById("mynetwork");
            var network = new vis.Network(container, data, options);


            /*-------------- 製作all table的 div 與專屬id ------------------ */
            var add_html = ''
            var add_herf = ''
            for (i=0 ;i< all_title_name.length;i++){
                /*--------------------------table 容器----------------------  */
                add_html = add_html + `<div id = ${column_order[i]}></div>`
                add_herf = add_herf + `<input id ="${column_order[i]}_move" class="btn btn-outline-primary" type="button" name="Submit" value="${column_order[i]}"  ></input>`
            }
            console.log(add_html)
            $('#herf_table').html(add_herf)
            $('#Answer2').html(add_html)
            for (i=0 ;i< all_title_name.length;i++){
                $(`#${column_order[i]}`).html(`<div class ="fs-3">Feature Name : ${column_order[i]}</div><div>${response.all_tables[column_order[i]]}</div>`)
                $(`#${column_order[i]}_table`).DataTable({
                    'columnDefs':[
                        {   'targets':-1,
                            'data':null,
                            render:function(row){
                                return '<a href = "/yeast/associated/detail/?id='+ table_name + '$' + row_name +'&name='+ all_title_name[i]+ '$' +row[1]+'"> Detail </a>';
                            },
                        },
                        {   'targets':2,
                            render:function(data,type,row,meta){
                                // console.log(row)
                                a_num = data.split('/')[0]
                                b_num = data.split('/')[1]
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${table_name}%${row_name}%${column_order[i]}%${row[1]}" > ${a_num} </a><a>/${b_num}</a>`
                            },
                        }
                    ]
                })
            }
            /*------------------------modal-----------------------*/
            $('.modal_features').on("click",function(){
                var feature_name = $(this).attr('value');
                console.log(feature_name)
                $.ajax({
                    url : '/yeast/ajax_modal/',
                    data : {'feature_name' : feature_name},
                    success:function(response){
                        console.log(response.evidence_table)
                        $('#modal_table').html(response.evidence_table)
                        $('#evidence_table').DataTable()
                    },
                    error :function(){
                        alert('Something error');
                    }
                })

            })
        },
        error :function(){
            alert('Something error');
        }
    })


})

$(document).on('click','input:button',function(){
    console.log($(this).attr('id').replace('_move',''))
    window.location.href = `#${$(this).attr('id').replace('_move','')}`




});
// $(document).on('click','#GO_CC_move ',function(){
//     window.location.href = "#GO_CC";
// });
// $(document).on('click','#GO_BP_move ',function(){
//     window.location.href = "#GO_CC";
// });