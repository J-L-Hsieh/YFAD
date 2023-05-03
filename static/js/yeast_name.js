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
    var first_feature_array = first_feature.split('$')
    var second_feature_array = second_feature.split('$')
    console.log(first_feature_array)
    console.log(second_feature_array)

    $('#first').html(`<h4 ><a>The qureied term </a> <a style="color:red"> ${first_feature_array[0]} </a> <a> from the feature</a><a style="color:red"> ${first_feature_array[2]}</a></h4>`)
    $('#second').html(`<h4 ><a>The associated term </a> <a style="color:red"> ${second_feature_array[0]} </a> <a> from the feature</a><a style="color:red"> ${second_feature_array[2]}</a></h4>`)

    $.ajax({
        url : '/yeast/ajax_name/',
        data : { 'first_feature' : first_feature,'second_feature' : second_feature },
        success:function(response){
            // -------------------------table1---------------
            $('#table1').html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header">table1</h3><div class="card-body">${response.both_contain}</div></div>`)
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
            $('#table2').html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header">table2</h3><div class="card-body">${response.queried_contain}</div></div>`)
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
                                return `<a class="modal_features" href = "#exampleModal" data-bs-toggle="modal" value="${first_feature_array[0]}%${first_feature_array[1]}%${second_feature_array[0]}%${second_feature_array[1]}%${row[0]}"}"> Evidence </a>`
                            }
                        },
                    },
                ]
            })
            // -------------------------table2---------------
            // -------------------------table3---------------
            $('#table3').html(`<div class="card" style="margin-top:5%;" ><h3 class ="fs-3 card-header">table3</h3><div class="card-body">${response.second_contain}</div></div>`)
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
            $('#queried_term').html(`<h5>Queried Feature : ${first_feature_array[1]}</h5>`)
            $('#queried_num').html(`<h5>Number:${trs1.length+trs3.length-2}</h5>`)
            $('#queried_last').html(`<h5>${trs3.length-1}</h5>`)

            $('#compare_term').html(`<h5>Comapre Feature : ${second_feature_array[1]}</h5>`)
            $('#compare_num').html(`<h5>Number:${trs1.length+trs2.length-2}</h5>`)
            $('#compare_last').html(`<h5>${trs2.length-1}</h5>`)

            $('#intersection_num').html(`<h5>${trs1.length-1}</h5>`)

            // -------------------modal table1---------------
            $('#both_name_table').on("click",'.modal_features',function(){
                var feature = $(this).attr('value');
                var exist = feature.split('%')
                var feature1_exist = exist[0]
                var feature2_exist = exist[2]
                console.log(exist)

                $.ajax({
                    url : '/yeast/ajax_evidence/',
                    data : {'feature' : feature},
                    success:function(response){
                        if (feature1_exist != 'false'){
                            $('#feature1').html(response.feature1_table)
                            $('#feature1_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#feature1').html('<div></div>')
                        }
                        if (feature2_exist != 'false'){
                            $('#feature2').html(response.feature2_table)
                            $('#feature2_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#feature2').html('<div></div>')
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
                console.log(exist)

                $.ajax({
                    url : '/yeast/ajax_evidence/',
                    data : {'feature' : feature},
                    success:function(response){
                        if (feature1_exist != 'false'){
                            $('#feature1').html(response.feature1_table)
                            $('#feature1_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#feature1').html('<div></div>')
                        }
                        if (feature2_exist != 'false'){
                            $('#feature2').html(response.feature2_table)
                            $('#feature2_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#feature2').html('<div></div>')
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
                console.log(exist)

                $.ajax({
                    url : '/yeast/ajax_evidence/',
                    data : {'feature' : feature},
                    success:function(response){
                        if (feature1_exist != 'false'){
                            $('#feature1').html(response.feature1_table)
                            $('#feature1_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#feature1').html(' ')
                        }
                        if (feature2_exist != 'false'){
                            $('#feature2').html(response.feature2_table)
                            $('#feature2_table').DataTable({
                                'bAutoWidth':true,
                                // 'scrollX':true,
                                // 'scrollY':true,
                            })
                        }
                        else{
                            $('#feature2').html(' ')
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