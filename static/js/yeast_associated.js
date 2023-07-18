$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
})

feature_dict = {"GO_MF":"GO_MF", "GO_BP":"GO_BP", "GO_CC":"GO_CC", "Protein_Domain":"Protein Domain", "Mutant_Phenotype":"Mutant Phenotype", "Pathway":"Pathway", "Disease":"Disease", "Transcriptional_Regulation":"Transcriptional Regulation", "Physical_Interaction":"Physical Interaction", "Genetic_Interaction":"Genetic Interaction"}

$(document).ready(function(){
    $('a[data-toggle="tab"]').on( 'shown.bs.tab', function (e) {
        $($.fn.dataTable.tables( true ) ).css('width', '100%');
        $($.fn.dataTable.tables( true ) ).DataTable().columns.adjust().draw();
    } );
    /*----- chage table and network-----*/
    // $('#view_network').hide()

    $('#button_table').on('click', function(){
        $('#view_network').hide()
        $('#view_table').show()
        $('#button_table').addClass("active")
        $('#button_network').removeClass("active")

    });
    $('#button_network').on('click', function(){
        $('#view_table').hide()
        $('#view_network').show()
        $('#button_table').removeClass("active")
        $('#button_network').addClass("active")
    });
    /*----- chage table and network-----*/

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id = urlParams.get('id')
    const name = urlParams.get('name')
    const query = urlParams.get('query')
    $('#queried').html(`<h2>The queried term <a style="color:red;">${name}</a> from [${feature_dict[query]}]<h2>`)
    $('#associated_title').html(`<h4><a># of terms (from each feature) that are </a><a style="color:#007bff;">ASSOCIATED </a><a>with the queried term </a><a style="color:red;">${name} </a>from [${feature_dict[query]}]</h4>`)
    // console.log(name)
    $.ajax({
        url : '/yeast/ajax_network/',
        data : {'query':query, 'id':id, 'name':name},
        success:function(response){
            var column_order = response.column_order;
            var network_judge = false;
            /* --------------------------network graph----------------------------*/
            const nodeFilterValue = {
                main: true,
                GO_MF: false,
                GO_BP: false,
                GO_CC: false,
                Protein_Domain: false,
                Mutant_Phenotype: false,
                Pathway: false,
                Disease: false,
                Transcriptional_Regulation: false,
                Physical_Interaction: false,
                Genetic_Interaction: false,
            };
            for (i=1 ;i<column_order.length; i++){
                $('#nodeFilterSelect').append(`<option value="${column_order[i]}">${feature_dict[column_order[i]]}</option>`)
                if (i==1){
                    nodeFilterValue[column_order[i]] = true;
                }
                // if(i<6){
                //     $('#checkbox_container1').append(`<div style="width: 20%;" class="flexbox"><input type="checkbox" name="nodeFilterSelect" value=${column_order[i]} checked>${column_order[i]}</input></div>`)
                // }else{
                //     $('#checkbox_container2').append(`<div style="width: 20%;" class="flexbox"><input type="checkbox" name="nodeFilterSelect" value=${column_order[i]} checked>${column_order[i]}</input></div>`)
                // }
            }
            const nodeFilterSelector = document.getElementById("nodeFilterSelect");
            console.log(nodeFilterSelector)

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

            network.on("afterDrawing", function(){
                unLoading_mask();
            });

            }

            // create an array with nodes
            var nodes = new vis.DataSet(response.network_data.nodes);
            // create an array with edges
            var edges = new vis.DataSet(response.network_data.edges);
            //--------全部都顯示------
            // let nodeFilterValue = ""

            //--------全部都顯示------

            const nodesFilter = (node) =>{
            //     switch (nodeFilterValue){
            //         case "GO_MF":
            //             return node.type ==="GO_MF";
            //         case "GO_BP":
            //             return node.type ==="GO_BP";
            //         case "GO_CC":
            //             return node.type ==="GO_CC";
            //         case "Protein_Domain":
            //             return node.type ==="Protein_Domain";
            //         case "Mutant_Phenotype":
            //             return node.type ==="Mutant_Phenotype";
            //         case "Pathway":
            //             return node.type ==="Pathway";
            //         case "Disease":
            //             return node.type ==="Disease";
            //         case "Transcriptional_Regulation":
            //             return node.type ==="Transcriptional_Regulation";
            //         case "Physical_Interaction":
            //             return node.type ==="Physical_Interaction";
            //         case "Genetic_Interaction":
            //             return node.type ==="Genetic_Interaction";
            //     }
                return nodeFilterValue[node.type];
            }

            var nodesView = new vis.DataView(nodes, { filter : nodesFilter });
            var edgesView = new vis.DataView(edges);
            console.log(edgesView)

            nodeFilterSelector.addEventListener("change", (e)=>{
                // const { value, checked } = e.target;
                all_features = ["GO_MF", "GO_BP", "GO_CC", "Protein_Domain", "Mutant_Phenotype", "Pathway", "Disease", "Transcriptional_Regulation", "Physical_Interaction", "Genetic_Interaction"]
                for (i=0; i<10; i++){
                    if (all_features[i] == e.target.value){
                        nodeFilterValue[e.target.value] = true;
                    }else{
                        nodeFilterValue[all_features[i]] = false;
                    }
                }
                nodesView.refresh();
                startNetwork({ nodes: nodesView, edges: edgesView });

            })
            //-------check box--------

            // nodeFilterSelector.forEach((filter) =>
            //     filter.addEventListener("change", (e) => {
            //         const { value, checked } = e.target;
            //         nodesFilterValues[value] = checked;
            //         nodesView.refresh();
            //     })
            // );
            //-------check box--------

            startNetwork({ nodes: nodesView, edges: edgesView });

            $('#button_network').on('click', function(){
                if (network_judge == false){
                    Loading_mask();
                    startNetwork({ nodes: nodesView, edges: edgesView });
                    network_judge = true;
                }
                // unLoading_mask()
            });
        },
        error :function(){
            alert('Something error');
        },
    })




    $.ajax({
        url : '/yeast/ajax_associated/',
        data : {'query':  query, 'id':id, 'name':name},
        success:function(response){
            // console.log('-----')
            var column_order = response.all_tables.column_order;
            // console.log(column_order)
            let target_num = Array.from({ length: column_order.length }, (val, index) => index + 1);
            var feature_num = [];
            console.log(target_num)
            $('#Answer1').html(response.associated_table);
            var associated_table = $('#associated_table').DataTable({
                    "autoWidth": false,
                    'scrollY':true,
                    'scrollX':true,
                    'scrollCollapse': true,
                    fixedHeader: {
                        header: true,
                        footer: true,
                    },
                'columnDefs':[
                    {   'targets': 0,
                        render:function(data,type,row,meta){
                            return `<a"> ${data} </a>`
                        },
                    },
                    {   'targets': target_num,
                        render:function(data,type,row,meta){
                            feature_num.push(data);
                            return `<a id ="${column_order[meta.col-1]}_move" href="#${column_order[meta.col-1]}" name="Submit" value="${column_order[i]}"  >${data}</a>`

                    //             return `<input id ="${row[0]}_move" class="btn btn-primary" type="button" style="margin:2px;" name="Submit" value="${row[0]}"  ></input>`
                    //         data = eval(data)
                    //         var icon_data = data.map(item => '<a style="font-size: 2em; color:blue">· </a>'+ item+'<br>'.replace(/,/g,"___")).toString();
                    //         console.log(typeof(icon_data))
                    //         icon_data = icon_data.replace(/,/g," ").replace(/___/g,",");
                    //         return `<a> ${icon_data} </a>`
                    //         // if (data.length > 3){
                    //         //     hide_data = data.slice(2)
                    //         //     return `<a > ${data[0]}, ${data[1]}, ${data[2]}</a><br>
                    //         //     <span>
                    //         //         <i data-bs-toggle="collapse" id="plus${meta.col}_${meta.row}" class="fa fa-plus-circle" style="color:darkblue" aria-hidden="true"></i>
                    //         //     </span>
                    //         //     <span class="collapse" id="hide${meta.col}_${meta.row}" style='display:none'>
                    //         //         <i data-bs-toggle="collapse" id="minus${meta.col}_${meta.row}"class="fa fa-minus-circle" style="color:darkblue" aria-hidden="true"></i>
                    //         //         ${hide_data}
                    //         //     </span>
                    //         //     `
                    //         // }else{
                    //         //     return `<a> ${data} </a>`;
                    //         // }
                        },
                    },
                ]
            });

            function PlusHide(){
                $(document).ready(function(){
                    var plus = document.querySelectorAll('.fa-plus-circle');
                    plus.forEach(function(element){
                        element.addEventListener('click', function(event){
                            var coordinate = this.id.replace('plus','')
                            this.style.display = 'none';
                            $(`#hide${coordinate}`).show()
                        })
                    });
                })
            };

            function MinusHide(){
                $(document).ready(function(){
                    var minus = document.querySelectorAll('.fa-minus-circle');
                    minus.forEach(function(element){
                        // console.log(element)
                        element.addEventListener('click', function(event){
                            var coordinate = this.id.replace('minus','')
                            $(`#hide${coordinate}`).hide();
                            $(`#plus${coordinate}`).show();
                        })
                    })
                })
            };

            PlusHide();
            MinusHide();
            associated_table.on('page.dt',function(){
                PlusHide();
                MinusHide();
            })


            /*-------------- 製作all table的 div 與專屬id ------------------ */
            var add_html = ''
            var add_href = ''
            for (i=0 ;i< column_order.length;i++){
                /*--------------------------table 容器----------------------  */
                add_html = add_html + `<div id = ${column_order[i]}></div>`
                add_href = add_href + `<input id ="${column_order[i]}_move" class="btn btn-primary" type="button" style="margin:2px;" name="Submit" value="${column_order[i]}"  ></input>`
            }
            // console.log(feature_num)
            $('#href_table').html(`<h4>The terms (from each feature) that are <a style="color:#007bff;">ASSOCIATED </a>with the queried term <a style="color:red;">${name} </a>from [${feature_dict[query]}]</h4>`)

            $('#Answer2').html(add_html)
            for (i=0 ;i< column_order.length;i++){
                if (feature_num[i]==1){
                    $(`#${column_order[i]}`).html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header"><a style="color:red">${feature_num[i]} term </a> from [${feature_dict[column_order[i]]}] <a> is</a><a style="color:#007bff"> ASSOCIATED</a> with the queried term <a style="color:red"> ${name}</a> from [${feature_dict[query]}]</h3> <div class="card-body">${response.all_tables[column_order[i]]}</div></div>`)
                }else{
                    $(`#${column_order[i]}`).html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header"><a style="color:red">${[feature_num[i]]} terms </a> from [${feature_dict[column_order[i]]}] <a> are</a><a style="color:#007bff"> ASSOCIATED</a> with the queried term <a style="color:red"> ${name}</a> from [${feature_dict[query]}]</h3> <div class="card-body">${response.all_tables[column_order[i]]}</div></div>`)
                }
                $(`#${column_order[i]}_table`).DataTable({
                    'columnDefs':[
                        {   'targets':-1,
                            render:function(data,type,row,meta){
                                var second_name = row[1].split('*')[0]
                                return `<a href = "/yeast/browse/associated/detail/?query=${query}*${id}*${name}&associate=${column_order[i]}*${data}*${second_name}" target="_blank"> Detail </a>`;
                            },
                        },
                        {   'targets':0,
                        render:function(data,type,row,meta){
                            return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value = "${query}*${name}*${id}" target="_blank"> ${name} </a>`;
                        },
                        },
                        {   'targets':1,
                        render:function(data,type,row,meta){
                            var data = data.split('*')
                            var feature_name = data[0]
                            var feature_id = data[1]
                            return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value = "${column_order[i]}*${feature_name}*${feature_id}" target="_blank"> ${feature_name} </a>`;
                        },
                        },
                        // {   'targets':5,
                        //     render:function(data,type,row,meta){
                        //         // console.log(row)
                        //         return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${feature}%${id}%${column_order[i]}%${row[6]}" > ${data} </a></a>`
                        //     },
                        // }
                    ]
                })
            }
            /*------------------------modal-----------------------*/
            $('.modal_features').on("click",function(){
                var feature_name = $(this).attr('value');
                var feature = feature_name.split("*")[0];
                var name = feature_name.split("*")[1];
                $.ajax({
                    url : '/yeast/ajax_p1_modal/',
                    data : {'feature_name' : feature_name},
                    success:function(response){
                        // console.log(response.evidence_table)
                        $('#modal_table').html(response.evidence_table)
                        var table_row = evidence_table.rows.length-1;
                        $('#evidence_table').DataTable({
                            'bAutoWidth' : true,
                            // 'scrollX':true,
                            // 'scrollY' : true,
                            "scrollCollapse" : true,
                            "destroy": true,
                        })
                        if (feature =="Physical_Interaction"||feature =="Genetic_Interaction"){
                            $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the queried term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature_dict[query]}]: </a><a style="color:red;">${table_row} genes </a><a> have ${feature_dict[query].toLowerCase()} with <a style="color:red;">${name}</a>`)
                        }else if(feature =="Transcriptional_Regulation"){
                            $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the queried term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature_dict[query]}]: </a><a style="color:red;">${table_row} genes </a><a> are the targets of ${feature_dict[query].toLowerCase()} <a style="color:red;">${name}</a>`)
                        }else if(feature =="GO_MF"||feature =="GO_BP"||feature =="GO_CC"){
                            $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the queried term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature_dict[query]}]</a>`)
                        }else{
                            $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the queried term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature_dict[query]}]</a>`)
                        }

                    },

                    error :function(){
                        alert('Something error');
                    }
                })
            })
            /*------------------------modal-----------------------*/
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
