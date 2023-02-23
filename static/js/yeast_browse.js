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
        var  table_name = document.getElementById('first').value
        $.ajax({
            url: '/yeast/ajax_yeast_browser/',
            data: input,
            success: function(response){
                $('#browse_result').show()
                // $('#result').html('<div class="container"><div class="card mt-5 w-100"><div class="card-body"></div>'+response.table+'</div></div>')
                $('#result').html('<div class="card"><div class="card-body"><table id="result_table" class="table table-bordered table-hover dataTable no-footer"></table></div></div>')
                // console.log(response.table)
                let target_num = Array.from({ length: response.columns.length-2 }, (val, index) => index + 1);
                console.log(target_num)
                    $('#result_table').DataTable({
                    // 'bAutoWidth':true,
                    // 'scrollX':true,
                    'scrollY':true,
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
                                                <i data-bs-toggle="collapse" href="#detail${meta.col}_${meta.row}" style="color:darkblue" class="fa fa-bars" aria-hidden="true"></i>
                                                <div class="collapse" id="detail${meta.col}_${meta.row}">
                                                    ${hide_data}
                                                </div>`
                                    }else{
                                        return `<a> ${data} </a>`;
                                    }
                                }
                            },
                        },
                        {   'targets':-1,
                            render:function(data, type, row, meta){
                                return '<a href = "/yeast/browse/associated/?id='+ data + '&name='+ row[0] +'&feature='+ table_name +'"> Detail </a>';
                            },
                        }
                    ]
                })
            },

            error: function(){
                alert('Something error');
            },
        });
    })
})