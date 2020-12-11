$(function(){
    $("#tab").on("click", ":button", function(event){
        $("#text").val($(this).closest("tr").find("td").eq(0).text());
    });
});