$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});

$(document).ready(function() {

    /* -------------------------------------下拉式選單與checkbox連動------------------------------------- */
    // var first = document.getElementById('first').value
    // console.log(first)
    // document.getElementById(`${first}`).style.display = 'none';
    // document.getElementById(`${first}_input`).checked = false;
    // console.log(typeof(first))
    // $('#first').on('change',function(){
    //     console.log(first)
    //     document.getElementById(`${first}`).style.display = '';  /* 顯現原有的 */
    //     document.getElementById(`${first}_input`).checked = true;

    //     first = this.value
    //     console.log(first)

    //     document.getElementById(`${first}`).style.display = 'none';  /*隱藏選到的 */
    //     document.getElementById(`${first}_input`).checked = false ;
    // });

    /* -----------------------------------------傳遞已選擇變數------------------------------------- */
    $('#submit_feature').click(function(e){
        e.preventDefault();
        var checkboxvalue = '&other_feature=';
        $("input[type=checkbox]:checked").each(function(i){
            checkboxvalue = checkboxvalue + ($(this).val()+',');
        });
        var input = $('#features').serialize() + checkboxvalue;
        var  table_name = document.getElementById('query_feature').value
        console.log(input)

        $.ajax({
            url: '/yeast/ajax_yeast_browser/',
            data: input,
            success: function(response){
                $('#browse_result').show()
                // $('#result').html('<div class="container"><div class="card mt-5 w-100"><div class="card-body"></div>'+response.table+'</div></div>')
                $('#result').html('<div class="card"><div class="card-body"><table id="result_table" class="table table-bordered table-hover dataTable no-footer"></table></div></div>')

                let target_num = Array.from({ length: response.columns.length-2 }, (val, index) => index + 1);

                var queried_feature = response.columns[0].title.replace(" (Queried)", "")

                    var result_table = $('#result_table').DataTable({
                    'order': [[1, 'desc']],

                    // 'bAutoWidth':true,
                    'scrollY':true,
                    'scrollX':true,
                    'scrollCollapse': true,
                    fixedHeader:           {
                        header: true,
                        footer: true,
                    },
                    data : response.table,
                    columns : response.columns,
                    'columnDefs':[
                        {   'targets': target_num,
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
                        {   'targets':0,
                            render:function(data, type, row, meta){
                                // return `<a id="mouse_touch${meta.row}" value="${meta.row}"> {data} </a>`;
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${queried_feature}*${data}*${row[row.length-1]}" > ${data} </a>`

                            },
                        },
                        {   'targets':-1,
                            render:function(data, type, row, meta){
                                return '<a href = "/yeast/browse/associated/?id='+ data + '&name='+ row[0] +'&query='+ table_name +'" target="_blank"> Detail </a>';
                            },
                        },
                    ]
                })

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
                    $('#modal_table').empty();
                    $('#modal_table_name').empty();

                    var feature = feature_name.split("*")[0];
                    var name = feature_name.split("*")[1];
                    // console.log(feature_name)
                    $.ajax({
                        url : '/yeast/ajax_p1_modal/',
                        data : {'feature_name' : feature_name},
                        success:function(response){
                            // console.log(response.evidence_table)
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

                            if (feature =="Physical_Interaction"||feature =="Genetic_Interaction"){
                                $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature.replace("_", " ")}]: </a><a style="color:red;">${table_row} genes </a><a> have ${feature.replace("_", " ").toLowerCase()} with <a style="color:red;">${name}</a>`)
                            }else if(feature =="Transcriptional_Regulation"){
                                console.log(feature)
                                $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature.replace("_", " ")}]: </a><a style="color:red;">${table_row} genes </a><a> are the targets of ${feature.replace("_", " ").toLowerCase()} <a style="color:red;">${name}</a>`)
                            }else if(feature =="GO_MF"||feature =="GO_BP"||feature =="GO_CC"){
                                $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature}]</a>`)
                            }else{
                                $("#modal_table_name").html(`<a style="color:red;">${table_row} genes</a><a> are annotated in the term [</a><a style="color:red;">${name}</a><a>] from the feature </a><a>[${feature.replace("_", " ")}]</a>`)
                            }

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
        });
    })
});
