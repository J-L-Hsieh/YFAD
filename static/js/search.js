$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});
$(document).ready(function() {

    $('#submit').click(function(){
        var input = $('#search_input').serialize();
        console.log(input)
        $.ajax({
            url: 'ajax_search/',
            data: $('#search_input').serialize(),
            success: function(response){
                let feature = response.feature
                $('#search_result').show()
                $('#result').html(`<div class="card"><div class="card-body"> ${response.table}</div></div>`);
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
                            return `<a id="mouse_touch${meta.row}" value="${meta.row}"> ${data} </a>`;
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
                                return '<a href = "/yeast/browse/associated/?id='+ data + '&name='+ row[0] +'&feature='+ feature +'"> Detail </a>';
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

                AddCountName();
                PlusHide();
                MinusHide();
                result_table.on('page.dt',function(){
                    AddCountName()
                    PlusHide();
                    MinusHide();
                })

            },



            error: function(){
                alert('Something error');
            },
        })
    })
})
