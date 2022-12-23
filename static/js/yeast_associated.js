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
            for (i=0 ;i<column_order.length; i++){
                $('#nodeFilterSelect').append(`<option value=${column_order[i]}>${column_order[i]}</option>`)
            }

            const nodeFilterSelector = document.getElementById("nodeFilterSelect");


            function startNetwork(data) {
            const container = document.getElementById("mynetwork");
            const options = {
                autoResize:true,

                interaction:{
                    hover: true
                },
                // nodes:{
                //     physics:false
                // },
                edges:{
                    arrows:{
                        to:{enabled:true, type: 'arrow'}
                    },
                }
            };
            const network = new vis.Network(container, data, options);

            // 設置固定位置設定

            network.on("dragEnd", function(params){
                if (params.nodes&&params.nodes.length > 0){
                    network.clustering.updateClusteredNode(params.nodes[0], {physics : false});
                }
            });
            }

            // create an array with nodes
            var nodes = new vis.DataSet(response.network_data.nodes);
            console.log(nodes)
            // create an array with edges
            var edges = new vis.DataSet(response.network_data.edges);

            let nodeFilterValue = "";

            const nodesFilter = (node) => {
            if (nodeFilterValue === "") {
                return true;
            }

            switch (nodeFilterValue) {
                case "GO_MF"||"main":
                return node.type === "GO_MF"|| node.type ==="main";
                case "GO_BP"||"main":
                return node.type === "GO_BP"|| node.type ==="main";
                case "GO_CC"||"main":
                return node.type === "GO_CC"|| node.type ==="main";
                case "Protein_Domain"||"main":
                return node.type === "Protein_Domain"|| node.type ==="main";
                case "Phenotype"||"main":
                return node.type === "Phenotype"|| node.type ==="main";
                case "Disease"||"main":
                return node.type === "Disease"|| node.type ==="main";
                case "Physical_Interaction"||"main":
                return node.type === "Physical_Interaction"|| node.type ==="main";
                case "Genetic_Interaction"||"main":
                return node.type === "Genetic_Interaction"|| node.type ==="main";
                case "Pathway"||"main":
                return node.type === "Pathway"|| node.type ==="main";
                case "Transcriptional_Regulation"||"main":
                return node.type === "Transcriptional_Regulation"|| node.type ==="main";
                default:
                return true;
            }
            };

            const nodesView = new vis.DataView(nodes, { filter: nodesFilter });
            const edgesView = new vis.DataView(edges);

            nodeFilterSelector.addEventListener("change", (e) => {
            // set new value to filter variable
            nodeFilterValue = e.target.value;

            nodesView.refresh();
            });

            startNetwork({ nodes: nodesView, edges: edgesView });


            /*-------------- 製作all table的 div 與專屬id ------------------ */
            var add_html = ''
            var add_herf = ''
            for (i=0 ;i< column_order.length;i++){
                /*--------------------------table 容器----------------------  */
                add_html = add_html + `<div id = ${column_order[i]}></div>`
                add_herf = add_herf + `<input id ="${column_order[i]}_move" class="btn btn-outline-primary" type="button" name="Submit" value="${column_order[i]}"  ></input>`
            }
            console.log(add_html)
            $('#herf_table').html(add_herf)
            $('#Answer2').html(add_html)
            for (i=0 ;i< column_order.length;i++){
                $(`#${column_order[i]}`).html(`<div class ="fs-3">Feature Name : ${column_order[i]}</div><div>${response.all_tables[column_order[i]]}</div>`)
                $(`#${column_order[i]}_table`).DataTable({
                    'columnDefs':[
                        {   'targets':-1,
                            'data':null,
                            render:function(row){
                                return '<a href = "/yeast/associated/detail/?id='+ table_name + '$' + row_name +'&name='+ column_order[i]+ '$' +row[1]+'"> Detail </a>';
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