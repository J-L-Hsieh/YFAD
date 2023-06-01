$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});
// modal內的datatable無法共用此設定
// var datatable_set ={'bAutoWidth':true,
//                     'scrollX':true,
//                     'scrollY':true,}

$(document).ready(function() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const first_feature = urlParams.get('id')
    const second_feature = urlParams.get('name')
    console.log(first_feature)
    var first_feature_array = first_feature.split('*')
    var second_feature_array = second_feature.split('*')
    console.log(first_feature_array)
    console.log(second_feature_array)

    $('#first').html(`<h4 ><a>The qureied term </a> <a style="color:red"> ${first_feature_array[2]} </a> <a> from [${first_feature_array[0]}]</a></h4>`)
    $('#second').html(`<h4 ><a>The associated term </a> <a style="color:red"> ${second_feature_array[2]} </a> <a> from [${second_feature_array[0]}]</a></h4>`)

    $.ajax({
        url : '/yeast/ajax_name/',
        data : { 'first_feature' : first_feature,'second_feature' : second_feature },
        success:function(response){
            // -------------------------table1---------------
            $('#table1').html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header"><a id="table1_header_num"></a>annotated <a style="color:red">BOTH</a> in the queried term & the associated term</h3><div class="card-body">${response.both_contain}</div></div>`)
            let trs1 = document.querySelectorAll('#both_name_table tr');

            for (let tr of trs1) {
                let td = document.createElement('td');
                tr.appendChild(td);
            }
            $('#both_name_table').DataTable({
                // 'scrollY':true,
                dom: 'Bfrtip',
                buttons: [
                'csv', 'pdf', 'print'
                ],
                'columnDefs':[
                    {   'targets':1,
                        render:function(row){
                            if (row ==='true'){
                                return '<i class="fa fa-check" aria-hidden="true" style="color:green"></i>'
                            }else{
                                return '<i class="fa fa-times" aria-hidden="true" style="color:red"></i>'
                            }
                        }
                    },
                    {   "target":2,
                        render: function(row){
                            if (row ==='true'){
                                return '<i class="fa fa-check" aria-hidden="true" style="color:green"></i>'
                            }else{
                                return '<i class="fa fa-times" aria-hidden="true" style="color:red"></i>'
                            }
                        }
                    },
                    {   'targets':3,
                        render:function(data,type,row,meta){
                            if (row[1] === 'false'){
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${row[1]}%${first_feature_array[1]}%${second_feature_array[0]}%${second_feature_array[1]}%${row[0]}"> Evidence </a>`
                            }else if(row[2] === 'false'){
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${first_feature_array[0]}%${first_feature_array[1]}%${row[2]}%${second_feature_array[1]}%${row[0]}"> Evidence </a>`
                            }
                            else{
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${first_feature_array[0]}%${first_feature_array[1]}%${second_feature_array[0]}%${second_feature_array[1]}%${row[0]}"}"> Evidence </a>`
                            }
                        },
                    },
                ],
            })
            // -------------------------table1---------------
            // -------------------------table2---------------
            $('#table2').html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header"><a id="table2_header_num"></a>annotated <a style="color:red">ONLY</a> in the queried term but <a style="color:red">NOT</a> in the associated term</h3><div class="card-body">${response.queried_contain}</div></div>`)
            let trs2 = document.querySelectorAll('#queried_table tr');

            for (let tr of trs2) {
                let td = document.createElement('td');
                tr.appendChild(td);
            }
            $('#queried_table').DataTable({
                // 'scrollY':true,
                dom: 'Bfrtip',
                buttons: [
                'csv', 'pdf', 'print'
                ],
                'columnDefs':[
                    {   'targets':1,
                        render:function(row){
                            if (row ==='true'){
                                return '<i class="fa fa-check" aria-hidden="true" style="color:green"></i>'
                            }else{
                                return '<i class="fa fa-times" aria-hidden="true" style="color:red"></i>'
                            }
                        }
                    },
                    {   "target":2,
                        render: function(row){
                            if (row ==='true'){
                                return '<i class="fa fa-check" aria-hidden="true" style="color:green"></i>'
                            }else{
                                return '<i class="fa fa-times" aria-hidden="true" style="color:red"></i>'
                            }
                        }
                    },
                    {   'targets':3,
                        render:function(data,type,row,meta){
                            if (row[1] === 'false'){
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${row[1]}%${first_feature_array[1]}%${second_feature_array[0]}%${second_feature_array[1]}%${row[0]}"> Evidence </a>`
                            }else if(row[2] === 'false'){
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${first_feature_array[0]}%${first_feature_array[1]}%${row[2]}%${second_feature_array[1]}%${row[0]}"> Evidence </a>`
                            }
                            else{
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${first_feature_array[0]}%${first_feature_array[1]}%${second_feature_array[0]}%${second_feature_array[1]}%${row[0]}"> Evidence </a>`
                            }
                        },
                    },
                ]
            })
            // -------------------------table2---------------
            // -------------------------table3---------------
            $('#table3').html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header"><a id="table3_header_num"></a>annotated <a style="color:red">ONLY</a> in the associated term but <a style="color:red">NOT</a> in the queried term</h3><div class="card-body">${response.second_contain}</div></div>`)
            let trs3 = document.querySelectorAll('#second_table tr');
            console.log(trs3)

            for (let tr of trs3) {
                let td = document.createElement('td');
                tr.appendChild(td);
            }
            $('#second_table').DataTable({
                // 'scrollY':true,
                dom: 'Bfrtip',
                buttons: [
                'csv', 'pdf', 'print'
                ],
                'columnDefs':[
                    {   'targets':1,
                        render:function(row){
                            if (row ==='true'){
                                return '<i class="fa fa-check" aria-hidden="true" style="color:green"></i>'
                            }else{
                                return '<i class="fa fa-times" aria-hidden="true" style="color:red"></i>'
                            }
                        }
                    },
                    {   "target":2,
                        render: function(row){
                            if (row ==='true'){
                                return '<i class="fa fa-check" aria-hidden="true" style="color:green"></i>'
                            }else{
                                return '<i class="fa fa-times" aria-hidden="true" style="color:red"></i>'
                            }
                        }
                    },
                    {   'targets':3,
                        render:function(data,type,row,meta){
                            if (row[1] === 'false'){
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${row[1]}%${first_feature_array[1]}%${second_feature_array[0]}%${second_feature_array[1]}%${row[0]}"> Evidence </a>`
                            }else if(row[2] === 'false'){
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${first_feature_array[0]}%${first_feature_array[1]}%${row[2]}%${second_feature_array[1]}%${row[0]}"> Evidence </a>`
                            }
                            else{
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${first_feature_array[0]}%${first_feature_array[1]}%${second_feature_array[0]}%${second_feature_array[1]}%${row[0]}"}"> Evidence </a>`
                            }
                        },
                    },
                ]
            })
            // -------------------------table3---------------
            $('#queried_term').html(`<h5>Queried term : ${first_feature_array[2]}</h5>`)
            $('#queried_num').html(`<h5>Number:${trs1.length+trs2.length-2}</h5>`)
            console.log(trs2.length-1)
            if (trs2.length-1 == 0){
                $('#queried_last').html(`<h5>${trs2.length-1}</h5>`)
            }else{
                $('#queried_last').html(`<h5><a href="#table2">${trs2.length-1}</a></h5>`)
000            }

            $('#compare_term').html(`<h5>Comapre term : ${second_feature_array[2]}</h5>`)
            $('#compare_num').html(`<h5>Number:${trs1.length+trs3.length-2}</h5>`)
            if (trs3.length-1 == 0){
                $('#compare_last').html(`<h5>${trs3.length-1}</h5>`)
            }else{
                $('#compare_last').html(`<h5><a href="#table3">${trs3.length-1}</a></h5>`)
            }

            $('#intersection_num').html(`<h5><a href="#table1">${trs1.length-1}</a><h5>`)

            $('#explain_text').html(`<h5>• ${trs1.length+trs3.length-2} genes are annotated in the queried term</h5><h5>• ${trs1.length+trs2.length-2} genes are annotated in the associated term</h5><h5>• ${trs1.length-1} genes are annotated both in the queried term & the associated term</h5>`)

            if (trs1.length-1 == 0||trs1.length-1 == 1){
                $('#table1_header_num').html(`${trs1.length-1} gene is `)
            }else{$('#table1_header_num').html(`${trs1.length-1} genes are `)}

            if (trs2.length-1 == 0||trs2.length-1 == 1){
                $('#table2_header_num').html(`${trs2.length-1} gene is `)
            }else{$('#table2_header_num').html(`${trs2.length-1} genes are `)}

            if (trs3.length-1 == 0||trs3.length-1 == 1){
                $('#table3_header_num').html(`${trs3.length-1} gene is `)
            }else{$('#table3_header_num').html(`${trs3.length-1} genes are `)}


            // -------------------modal table1---------------
            $('#both_name_table').on("click",'.modal_features',function(){
                var feature = $(this).attr('value');
                var exist = feature.split('%')
                var feature1_exist = exist[0]
                var feature2_exist = exist[2]
                var queried_term = exist[1]
                var associated_term = exist[3]
                var systematic_name = exist[4]

                console.log(exist)

                $.ajax({
                    url : '/yeast/ajax_evidence/',
                    data : {'feature' : feature},
                    success:function(response){
                        $('#modal_title').html(`${systematic_name} is annotated <a style="color:#007bff">BOTH</a> in the queried term <a style="color:red">${queried_term}</a> & the associated term <a style="color:red">${associated_term}</a>`)
                        if (feature1_exist != 'false'){
                            $('#modal_table1').show()
                            $('#modal_table1_header').html(`${systematic_name} is annotated in the queried term <a style="color:red">${queried_term}</a>`)
                            $('#feature1').html(response.feature1_table)
                            $('#feature1_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#modal_table1').hide()
                        }
                        if (feature2_exist != 'false'){
                            $('#modal_table2').show()
                            $('#modal_table2_header').html(`${systematic_name} is annotated in the queried term <a style="color:red">${associated_term}</a>`)
                            $('#feature2').html(response.feature2_table)
                            $('#feature2_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#modal_table2').hide()
                        }
                    },
                    error :function(){
                        alert('Something error');
                    }
                })
            })
            // -------------------modal table1---------------
            // -------------------modal table2---------------
            $('#queried_table').on("click",'.modal_features',function(){
                var feature = $(this).attr('value');
                var exist = feature.split('%')
                var feature1_exist = exist[0]
                var feature2_exist = exist[2]
                var queried_term = exist[1]
                var associated_term = exist[3]
                var systematic_name = exist[4]
                console.log(exist)

                $.ajax({
                    url : '/yeast/ajax_evidence/',
                    data : {'feature' : feature},
                    success:function(response){
                        $('#modal_title').html(`${systematic_name} is annotated <a style="color:#007bff">ONLY</a> in the queried term <a style="color:red">${queried_term}</a> but <a style="color:#007bff">NOT</a> in the associated term <a style="color:red">${associated_term}</a>`)
                        if (feature1_exist != 'false'){
                            $('#modal_table1').show()
                            $('#modal_table1_header').html(`${systematic_name} is annotated in the queried term <a style="color:red">${queried_term}</a>`)
                            $('#feature1').html(response.feature1_table)
                            $('#feature1_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#modal_table1').hide()
                        }
                        if (feature2_exist != 'false'){
                            $('#modal_table2').show()
                            $('#modal_table2_header').html(`${systematic_name} is annotated in the queried term <a style="color:red">${associated_term}</a>`)
                            $('#feature2').html(response.feature2_table)
                            $('#feature2_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#modal_table2').hide()
                        }
                    },
                    error :function(){
                        alert('Something error');
                    }
                })
            });
            // -------------------modal table2---------------
            // -------------------modal table3---------------
            $('#second_table').on("click",'.modal_features',function(){
                var feature = $(this).attr('value');
                var exist = feature.split('%')
                var feature1_exist = exist[0]
                var feature2_exist = exist[2]
                var queried_term = exist[1]
                var associated_term = exist[3]
                var systematic_name = exist[4]

                console.log(exist)

                $.ajax({
                    url : '/yeast/ajax_evidence/',
                    data : {'feature' : feature},
                    success:function(response){
                        $('#modal_title').html(`${systematic_name} is annotated <a style="color:#007bff">ONLY</a> in the associated term <a style="color:red">${associated_term}</a> but <a style="color:#007bff">NOT</a> in the queried term <a style="color:red">${queried_term}</a>`)
                        if (feature1_exist != 'false'){
                            $('#modal_table1').show()
                            $('#modal_table1_header').html(`${systematic_name} is annotated in the queried term <a style="color:red">${queried_term}</a>`)
                            $('#feature1').html(response.feature1_table)
                            $('#feature1_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#modal_table1').hide()
                        }
                        if (feature2_exist != 'false'){
                            $('#modal_table2').show()
                            $('#modal_table2_header').html(`${systematic_name} is annotated in the queried term <a style="color:red">${associated_term}</a>`)
                            $('#feature2').html(response.feature2_table)
                            $('#feature2_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#modal_table2').hide()
                        }
                    },
                    error :function(){
                        alert('Something error');
                    }
                })
            });
            // -------------------modal table3---------------
        },
        error:function(){
            alert('Something error');
        }
    })
})