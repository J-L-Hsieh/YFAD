$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
})



$(document).ready(function(){
    $('a[data-toggle="tab"]').on( 'shown.bs.tab', function (e) {
        $($.fn.dataTable.tables( true ) ).css('width', '100%');
        $($.fn.dataTable.tables( true ) ).DataTable().columns.adjust().draw();
    } );
    /*----- chage table and network-----*/
    $('#view_network').hide()

    $('#button_table').on('click', function(){
        $('#view_network').hide()
        $('#view_table').show()
    });
    $('#button_network').on('click', function(){
        $('#view_table').hide()
        $('#view_network').show()
    });
    /*----- chage table and network-----*/

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id = urlParams.get('id')
    const name = urlParams.get('name')
    const feature = urlParams.get('feature')
    $('#queried').html(`<h2>Queried ${feature} Term : ${name}<h2>`)
    $('#associated_title').html(`<h4>Associated Term with the Queried ${feature} Term </h4>`)
    // console.log(name)
    $.ajax({
        url : '/yeast/ajax_network/',
        data : {'feature':feature, 'id':id, 'name':name},
        success:function(response){
            var column_order = response.column_order

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

                nodes:{
                    borderWidth:0.8,
                },

                edges:{
                    arrows:{
                        to:{enabled : true, type : 'arrow'}
                    },
                }
            };
            const network = new vis.Network(container, data, options);

            // ----設置固定位置設定-----
            network.on("stabilizationIterationsDone", function () {
                network.setOptions( { physics: false } );
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


        },
        error :function(){
            alert('Something error');
        },
    })
    $.ajax({
        url : '/yeast/ajax_associated/',
        data : {'feature':feature, 'id':id, 'name':name},
        success:function(response){
            // console.log('-----')
            var column_order = response.all_tables.column_order
            console.log(column_order)
            let target_num = Array.from({ length: column_order.length }, (val, index) => index + 1);
            $('#Answer1').html(response.associated_table);
            $('#associated_table').DataTable({
                'scrollY':true,
                'scrollX':true,
                'scrollCollapse': true,
                fixedHeader:{
                    header: true,
                    footer: true,
                },
                'columnDefs':[
                    {   'targets': target_num,
                        render:function(data,type,row,meta){
                            data = eval(data)
                            if (data.length > 3){
                                hide_data = data.slice(2)
                                return `<a > ${data[0]}, ${data[1]}, ${data[2]}</a><br>
                                        <div data-bs-toggle="collapse" href="#detail${meta.col}_${meta.row}" >
                                            <i href="#detail${meta.col}_${meta.row}" class=" fa fa-plus" style="color:darkblue" aria-hidden="true"></i>
                                        </div>
                                        <div class="collapse" id="detail${meta.col}_${meta.row}">
                                            <i data-bs-toggle="collapse" href="#detail${meta.col}_${meta.row}" class=" fa fa-minus" style="color:darkblue" aria-hidden="true"></i>
                                            ${hide_data}
                                        </div>
                                        `
                            }else{
                                return `<a> ${data} </a>`;
                            }
                        },
                    },
                ]
            });

            // console.log('---')
            // console.log(target_num)


            /*-------------- 製作all table的 div 與專屬id ------------------ */
            var add_html = ''
            var add_herf = ''
            for (i=0 ;i< column_order.length;i++){
                /*--------------------------table 容器----------------------  */
                add_html = add_html + `<div id = ${column_order[i]}></div>`
                add_herf = add_herf + `<input id ="${column_order[i]}_move" class="btn btn-primary" type="button" style="margin:2px;" name="Submit" value="${column_order[i]}"  ></input>`
            }
            // console.log(add_html)
            $('#herf_table').html(add_herf)
            $('#Answer2').html(add_html)
            for (i=0 ;i< column_order.length;i++){
                $(`#${column_order[i]}`).html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header">Feature Name : ${column_order[i]}</h3> <div class="card-body">${response.all_tables[column_order[i]]}</div></div>`)
                $(`#${column_order[i]}_table`).DataTable({
                    'columnDefs':[
                        {   'targets':-1,
                            render:function(data,type,row,meta){
                                var second_name = row[1].split('>')[1].replace('</a', '')
                                return '<a href = "/yeast/browse/associated/detail/?id='+ feature + '$' + id + '$' + name +'&name='+ column_order[i]+ '$' + data + '$' + second_name +'"> Detail </a>';
                            },
                        },
                        {   'targets':2,
                            render:function(data,type,row,meta){
                                // console.log(row)
                                var second_name = row[1].split('>')[1].replace('</a', '')

                                a_num = data.split('/')[0]
                                b_num = data.split('/')[1]
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${feature}%${id}%${column_order[i]}%${row[5]}" > ${a_num} </a><a>/${b_num}</a>`
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
                            'bAutoWidth' : true,
                            // 'scrollX':true,
                            // 'scrollY' : true,
                            "scrollCollapse" : true,
                            "destroy": true,
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
        },

    })


})

$(document).on('click','input:button',function(){
    // console.log($(this).attr('id').replace('_move',''))
    window.location.href = `#${$(this).attr('id').replace('_move','')}`



});
