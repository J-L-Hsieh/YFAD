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
            // console.log('-----')

            $('#Answer1').html(response.associated_table);
            $('#associated_table').DataTable();
            var column_order = response.all_tables.column_order


            /* --------------------------network graph----------------------------*/
            for (i=0 ;i<column_order.length; i++){
                if(i<5){
                    $('#checkbox_container1').append(`<div style="width: 20%;" class="flexbox"><input type="checkbox" name="nodeFilterSelect" value=${column_order[i]} checked>${column_order[i]}</input></div>`)
                }else{
                    $('#checkbox_container2').append(`<div style="width: 20%;" class="flexbox"><input type="checkbox" name="nodeFilterSelect" value=${column_order[i]} checked>${column_order[i]}</input></div>`)
                }
            }
            const nodeFilterSelector = document.getElementsByName("nodeFilterSelect");


            function startNetwork(data) {
            const container = document.getElementById("mynetwork");
            const options = {
                autoResize:true,

                interaction:{
                    hover: true
                },
                edges:{
                    arrows:{
                        to:{enabled : true, type : 'arrow'}
                    },
                }
            };
            const network = new vis.Network(container, data, options);

            // ----設置固定位置設定-----
            network.on("dragEnd", function(params){
                if (params.nodes&&params.nodes.length > 0){
                    network.clustering.updateClusteredNode(params.nodes[0], {physics : false});
                }
            });
            // ----設置固定位置設定-----

            }

            // create an array with nodes
            var nodes = new vis.DataSet(response.network_data.nodes);
            // create an array with edges
            var edges = new vis.DataSet(response.network_data.edges);

            //--------全部都顯示------
            const nodesFilterValues = {
                main: true,
                GO_MF: true,
                GO_BP: true,
                GO_CC: true,
                Protein_Domain: true,
                Mutant_Phenotype: true,
                Pathway: true,
                Disease: true,
                Transcriptional_Regulation: true,
                Physical_Interaction: true,
                Genetic_Interaction: true,
            };
            //--------全部都顯示------

            const nodesFilter = (node) =>{
                return nodesFilterValues[node.type];
            }

            const nodesView = new vis.DataView(nodes, { filter : nodesFilter });
            const edgesView = new vis.DataView(edges);
            console.log(edgesView)

            nodeFilterSelector.forEach((filter) =>
                filter.addEventListener("change", (e) => {
                    const { value, checked } = e.target;
                    nodesFilterValues[value] = checked;
                    nodesView.refresh();
            })
            );

            startNetwork({ nodes: nodesView, edges: edgesView });


            /*-------------- 製作all table的 div 與專屬id ------------------ */
            var add_html = ''
            var add_herf = ''
            for (i=0 ;i< column_order.length;i++){
                /*--------------------------table 容器----------------------  */
                add_html = add_html + `<div id = ${column_order[i]}></div>`
                add_herf = add_herf + `<input id ="${column_order[i]}_move" class="btn btn-outline-primary" type="button" name="Submit" value="${column_order[i]}"  ></input>`
            }
            // console.log(add_html)
            $('#herf_table').html(add_herf)
            $('#Answer2').html(add_html)
            for (i=0 ;i< column_order.length;i++){
                $(`#${column_order[i]}`).html(`<div class ="fs-3">Feature Name : ${column_order[i]}</div><div>${response.all_tables[column_order[i]]}</div>`)
                $(`#${column_order[i]}_table`).DataTable({
                    'columnDefs':[
                        {   'targets':-1,
                            'data':null,
                            render:function(data,type,row,meta){
                                return '<a href = "/yeast/browse/associated/detail/?id='+ table_name + '$' + row_name +'&name='+ column_order[i]+ '$' +row[1]+'"> Detail </a>';
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
                $.ajax({
                    url : '/yeast/ajax_modal/',
                    data : {'feature_name' : feature_name},
                    success:function(response){
                        // console.log(response.evidence_table)
                        $('#modal_table').html(response.evidence_table)
                        $('#evidence_table').DataTable({
                            'bAutoWidth':true,
                            'scrollX':true,
                            'scrollY':true,
                        })
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
    // console.log($(this).attr('id').replace('_move',''))
    window.location.href = `#${$(this).attr('id').replace('_move','')}`




});
// $(document).on('click','#GO_CC_move ',function(){
//     window.location.href = "#GO_CC";
// });
// $(document).on('click','#GO_BP_move ',function(){
//     window.location.href = "#GO_CC";
// });