$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});
$(document).ready(function() {
    //------search (change feature)------
    // var select_feature = document.getElementById("select_feature");
    // var chage_example = document.getElementById("example")
    // console.log(select_feature)

    // select_feature.onchange = function(){
    //     var feature = select_feature.value;
    //     switch (feature){
    //         case 'GO_MF':
    //             chage_example.innerHTML = "Y-form DNA binding";
    //             break;
    //         case 'GO_BP':
    //             chage_example.innerHTML = "zymogen activation";
    //             break;
    //         case 'GO_CC':
    //             chage_example.innerHTML = "vacuole";
    //             break;
    //         case 'Protein_Domain':
    //             chage_example.innerHTML = "MutS domain V";
    //             break;
    //         case 'Mutant Phenotype':
    //             chage_example.innerHTML = "inviable";
    //             break;
    //         case 'Pathway':
    //             chage_example.innerHTML = "glycolysis";
    //             break;
    //         case 'Disease':
    //             chage_example.innerHTML = "cancer";
    //             break;
    //         case 'Transcriptional_Regulation':
    //             chage_example.innerHTML = "SIN4";
    //             break;
    //         case 'Physical_Interaction':
    //             chage_example.innerHTML = "RPN11";
    //             break;
    //         case 'Genetic_Interaction':
    //             chage_example.innerHTML = "ADH3";
    //             break;
    //     }
    // }
    //------search (change feature)------

    $('#submit').click(function(){

        var term_name = $("#term_name").val(); //Y-form DNA binding
        var feature = $("#select_feature").val(); //GO_MF
        // console.log($('#search_input').serialize())
        $.ajax({
            url: 'ajax_search/',
            data: $('#search_input').serialize(),
            success: function(response){
                var find_feature = response.find_feature
                var add_nav = ''
                var chosen_featute
                for (i=0; i<find_feature.length; i++){
                    add_nav = add_nav + `<li class="nav-item"><a class="nav-link show_hide_table" value="${find_feature[i]}">${find_feature[i]}</a></li>`
                    $(`#${find_feature[i]}`).html(response.all_table[i])
                    $(`#${find_feature[i]}_table`).DataTable({
                        'scrollY':true,
                        'scrollX':true,
                        'scrollCollapse': true,
                        fixedHeader:{
                            header: true,
                            footer: true,
                        },
                        'columnDefs':[
                            {   'targets':-1,
                            render:function(data,type,row,meta){
                                return `<a href = "/yeast/browse/associated/?id=${data}&name=${row[0]}&feature=${find_feature[i]}" target="_blank"> Detail </a>`;
                            },
                        },
                        ]
                    })
                    if (i==0){
                        $(`#${find_feature[0]}`).show()
                        chosen_featute = find_feature[0]
                    }
                }
                // console.log(add_nav)
                $('#nav_header').html(add_nav);
                // -------show and hide different feature table-------
                $('.show_hide_table').on("click", function(){
                    $(`#${chosen_featute}`).hide();
                    chosen_featute = $(this).attr('value');
                    $(this)
                    $(`#${chosen_featute}`).show();
                })
                // -------show and hide different feature table-------

                var search_feature = document.getElementById("search_feature");
                search_feature.innerHTML = feature;
                var search_name = document.getElementById("search_name")
                search_name.innerHTML = term_name;

                $('#search_result').show()
                // $('#result').html(`<div class="card"><div class="card-body"> ${response.table}</div></div>`);
                // /*--------add column------*/
                // let trs = document.querySelectorAll('#result_table tr');

                // for (let tr of trs) {
                //     let td = document.createElement('td');
                //     tr.appendChild(td);
                // }
                // /*--------add column------*/

                var result_table = $('#result_table').DataTable({
                    'scrollY':true,
                    'scrollX':true,
                    'scrollCollapse': true,
                    fixedHeader:{
                        header: true,
                        footer: true,
                    },
                    'columnDefs':[
                        {   'targets':0,
                        render:function(data, type, row, meta){
                            // return `<a id="mouse_touch${meta.row}" value="${meta.row}"> ${data} </a>`;
                            data = data.replace(term_name,`</span><span style="background-color:yellow">${term_name}</span><span>`)
                            // console.log(data)
                            return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${feature}%${row[row.length-1]}" ><span>${data}</span></a>`

                        },
                        },
                        {   'targets': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            render:function(data,type,row,meta){
                                if (data == '-'){
                                    return `<a> ${data} </a>`;
                                }else{
                                    data = eval(data)
                                    if (data.length > 3){
                                        hide_data = data.slice(2)
                                        return `<a > ${data[0]}, ${data[1]}, ${data[2]}</a><br>
                                        <span>
                                            <i data-bs-toggle="collapse" id="plus${meta.col}_${meta.row}" class="fa fa-plus-circle" style="color:darkblue" aria-hidden="true"></i>
                                        </span>
                                        <span class="collapse" id="hide${meta.col}_${meta.row}" style='display:none'>
                                            <i data-bs-toggle="collapse" id="minus${meta.col}_${meta.row}"class="fa fa-minus-circle" style="color:darkblue" aria-hidden="true"></i>
                                            ${hide_data}
                                        </span>
                                        `
                                    }else{
                                        return `<a> ${data} </a>`;
                                    }
                                }
                            },
                        },
                        {   'targets':-1,
                            render:function(data,type,row,meta){
                                return `<a href = "/yeast/browse/associated/?id=${data}&name=${row[0]}&feature=${feature}" target="_blank"> Detail </a>`;
                            },
                        },
                    ]
                });
                function AddCountName(){
                    // 抓取所有 id 開頭為 mouse_touch 的元素
                    // const mouse_element = document.querySelectorAll('#mouse_touch]');
                    // console.log(document)
                    //新增document ready來使處理非同步的問題,否則會抓取頁面還沒切換前的資訊
                    $(document).ready(function(){
                        var mouse_element = document.querySelectorAll('[id^=mouse_touch]');

                        // 使用循環綁定 mouseover 事件到每個元素
                        mouse_element.forEach(function(element){
                            element.addEventListener("mouseenter", function(event){
                                // console.log(element);
                                var num = element.id.replace('mouse_touch','')
                                // console.log(num)
                                var count_nameDiv = document.createElement("div");
                                count_nameDiv.innerHTML += `${response.count_name_table[num][0]} <br> ${response.count_name_table[num][1]}`;
                                count_nameDiv.style.position = "absolute";
                                var x = event.clientX; //滑鼠的x座標
                                var y = event.clientY; //滑鼠的y座標
                                var scrollX = window.pageXOffset; //水平滾動距離
                                var scrollY = window.pageYOffset; //垂直滾動距離
                                var newX = x + scrollX; //滾動後的x座標
                                var newY = y + scrollY; //滾動後的y座標
                                // console.log(newX,newY)
                                count_nameDiv.style.top = newY+ "px";
                                count_nameDiv.style.left = newX + "px";
                                count_nameDiv.style.backgroundColor = "lightgray";
                                count_nameDiv.style.border = "1px solid black";
                                count_nameDiv.style.padding = "5px";
                                // count_nameDiv.style.display = "block";

                                // console.log(count_nameDiv)
                                // 將元素添加到頁面中
                                document.body.appendChild(count_nameDiv);
                                // 綁定 mouseout 事件，當滑鼠移開時，刪除剛剛建立的元素
                                element.addEventListener("mouseleave", function() {
                                        document.body.removeChild(count_nameDiv)
                                });
                            });
                        });
                        return;
                        });
                };
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
                }

                function MinusHide(){
                    $(document).ready(function(){
                        var minus = document.querySelectorAll('.fa-minus-circle');
                        minus.forEach(function(element){
                            console.log(element)
                            element.addEventListener('click', function(event){
                                var coordinate = this.id.replace('minus','')
                                $(`#hide${coordinate}`).hide();
                                $(`#plus${coordinate}`).show();
                            })
                        })
                    })
                }

                // AddCountName();
                PlusHide();
                MinusHide();
                result_table.on('page.dt',function(){
                    // AddCountName()
                    PlusHide();
                    MinusHide();
                })
                /*------------------------modal-----------------------*/
                $('.modal_features').on("click",function(){
                    var feature_name = $(this).attr('value');
                    var feature = feature_name.split("%")[0];
                    var name = feature_name.split("%")[1];
                    console.log(feature);

                    $.ajax({
                        url : '/yeast/ajax_p1_modal/',
                        data : {'feature_name' : feature_name},
                        success:function(response){
                            // console.log(response.evidence_table.rows.length)
                            $('#modal_table').html(response.evidence_table)
                            var evidence_table = document.getElementById("evidence_table");
                            var table_row = evidence_table.rows.length-1;
                            $('#evidence_table').DataTable({
                                'bAutoWidth' : true,
                                // 'scrollX':true,
                                // 'scrollY' : true,
                                "scrollCollapse" : true,
                                "destroy": true,
                            })
                            $("#model_table_name").html(`<a>${table_row} </a><a>genes are annotated in the queried term </a><a style="color:red;">${name} </a><a>from the chosen feature </a><a style="color:red;">${feature}</a>`)

                        },

                        error :function(){
                            alert('Something error');
                        }
                    })
                })
                /*------------------------modal-----------------------*/
            },



            error: function(){
                alert('Something error');
            },
        })
    })
})
