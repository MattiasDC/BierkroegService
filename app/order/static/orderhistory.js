$(document).ready(function () {
    
    function deleteOrder(row, deletedCallback) {
        deletedCallback($.post($("#delete-order-url").data('url'), { 'id' : row.find('td:first').text() }))
    }

    loadTable([],
              deleteOrder,
              null,
              null,
              null,
              null)

    $("#btnNew").toggle()
    $(this).find(".edit").remove()

    $(".collapse").on('show.bs.collapse', function(){
      $("#"+$(this).attr("id")+"Btn").find(".fa").removeClass("fa-plus").addClass("fa-minus");
    }).on('hide.bs.collapse', function(){
      $("#"+$(this).attr("id")+"Btn").find(".fa").removeClass("fa-minus").addClass("fa-plus");
    });
})